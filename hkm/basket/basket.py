# -*- coding: utf-8 -*-
import random
from decimal import Decimal

from django.conf import settings
from django.utils import timezone

from hkm.basket.basket_line import BasketLine
from hkm.models.campaigns import CampaignCode, CampaignStatus, Campaign, CampaignUsageType
from hkm.models.models import PrintProduct, ProductOrder


class Basket(object):

    def get_basket_target_user(self, request):
        return (request.user if not request.user.is_anonymous() else None)

    def __init__(self, request):
        self.request = request
        self.user = self.get_basket_target_user(request)
        self._data = None
        self._product_cache = {}
        self._line_details_cache = {}
        self.dirty = False

    def load(self):
        if self._data is None:
            self._data = self.request.session.setdefault('basket', {})
            self.dirty = False
        return self._data

    def save(self):
        self.request.session['basket'] = self._data
        self.dirty = False

    def _initialize_line(self, picture, quantity=0):
        return {
            'line_id': str(random.randint(0, 0x7FFFFFFF)),
            'hkm_id': picture['hkm_id'],
            'order_pk': picture['order_pk'],
            'text': picture['text'],
            'quantity': int(quantity),
            'type': 1,
            'product_id': picture['product_id'],
            'record': picture.get('record', {})
        }

    def _find_line_data_for_product(self, picture_id):

        for line_data in self._raw_lines:
            if line_data.get('hkm_id') != picture_id:
                return line_data

    def _add_line(self, data_line):
        self.dirty = True
        data_line = getattr(data_line, 'data', data_line)
        if any(l['line_id'] == data_line['line_id'] for l in self._raw_lines):  # already in basket
            return

        self._raw_lines.append(data_line)
        self._processed_lines_cache = None
        self.clean_empty_lines()

    def add_picture(self, picture_data, quantity, extra=None):
        if not extra:
            extra = {}
        data_line = (self._find_line_data_for_picture(picture_data, extra) or self._initialize_line(picture_data))

        line = BasketLine(self, data_line)
        line.add_quantity(quantity)
        self.set_discount_campaigns()
        self._add_line(data_line)
        return line

    def _find_line_data_for_picture(self, picture, extra):
        for data_line in self._raw_lines:
            if picture['hkm_id'] == data_line['hkm_id']:
                return data_line


    def _get_processed_lines(self):
        lines = getattr(self, '_processed_lines_cache', None)
        if lines is None:
            lines = [BasketLine(self, line) for line in self._raw_lines]
            # apply discounts
            if lines:
                lines += self.get_processed_campaign_lines(lines)
            self._processed_lines_cache = lines
        return lines

    def get_processed_campaign_lines(self, basket_lines):
        basket_campaigns = self.data.get("campaign_ids", {})
        campaigns = Campaign.objects.filter(pk__in=basket_campaigns.keys())
        discount_lines = []
        self._data["free_shipping"] = False
        for campaign in campaigns:
            if campaign.free_shipping:
                self._data["free_shipping"] = True

        # if user is museum / kiosk user they should always have free shipping anyway
        if self.user.profile.is_museum:
                self._data["free_shipping"] = True

            data_line = {
                'line_id': str(random.randint(0, 0x7FFFFFFF)),
                'product_id': None,
                'order_pk': None,
                'type': 4,
                'can_remove': campaign.usage_type != CampaignUsageType.CODELESS,
                'quantity': 1,
                'code': basket_campaigns.get(str(campaign.pk)),
                'text': campaign.name,
                'discount_value': campaign.get_discount_value(basket_lines),
                'campaign_id': campaign.pk
            }

            discount_lines.append(BasketLine(self, data_line))
        return discount_lines

    def _get_data_lines(self):
        return self.data.setdefault('lines', [])

    def _set_data_lines(self, new_lines):
        self.data['lines'] = new_lines
        self.dirty = True
        self._processed_lines_cache = None

    def clean_empty_lines(self):
        new_lines = [l for l in self._raw_lines if l['quantity'] > 0]
        if len(new_lines) != len(self._raw_lines):
            self._raw_lines = new_lines

    def find_line_by_line_id(self, line_id):
        for line in self._raw_lines:
            if unicode(line.get("line_id")) == unicode(line_id):
                return line
        return None

    def get_order(self, order_id):
        if not order_id:
            return None

        try:
            if order_id not in self._line_details_cache:
                self._line_details_cache[order_id] = ProductOrder.objects.get(id=order_id)
            return self._line_details_cache[order_id]
        except PrintProduct.DoesNotExist:
            # Product has been deleted or something
            # => dump the basket
            self.clear_all()
            self.save()
            return None

    def get_product(self, product_id):
        """ Basket has a product object cache. This fetches a Product into it. """
        if not product_id:
            return None

        try:
            if product_id not in self._product_cache:
                self._product_cache[product_id] = PrintProduct.objects.get(id=product_id)
            return self._product_cache[product_id]
        except PrintProduct.DoesNotExist:
            # Product has been deleted or something
            # => dump the basket
            self.clear_all()
            self.save()
            return None

    def delete_line(self, line_id):
        line = self.find_line_by_line_id(line_id)
        if line:
            line["quantity"] = 0
            self._processed_lines_cache = None
            self.clean_empty_lines()
            return True
        return False

    def clear_all(self):
        self.data.clear()
        self._processed_lines_cache = None
        self.dirty = True

    def set_discount_campaigns(self, code=None):
        # All current campaigns
        campaigns = Campaign.objects.filter(
            status=CampaignStatus.ENABLED
        ).exclude(
            usable_from__gt=timezone.now()
        ).exclude(
            usable_to__lt=timezone.now()
        )

        available_campaigns = []

        # Matched be code
        available_campaigns += list(CampaignCode.objects.filter(
            code=code,
            status=CampaignStatus.ENABLED,
            campaign__in=campaigns
        ).values_list('campaign__pk', 'code'))

        # Matched by time, codeless campaing.
        available_campaigns += list(campaigns.filter(usage_type=CampaignUsageType.CODELESS).values_list('pk',))
        campaign_ids = self.data.get("campaign_ids", {})
        for campaign in available_campaigns:
            campaign_ids[str(campaign[0])] = campaign[1] if len(campaign) > 1 else None

        self.data["campaign_ids"] = campaign_ids
        self._processed_lines_cache = None  # uncache basket
        self.save()

    def remove_campaign(self, campaign_pk_to_remove):
        """
        :type campaign_to_remove: Campaign
        """
        self.data["campaign_ids"].pop(str(campaign_pk_to_remove))
        self._processed_lines_cache = None  # uncache basket
        self.save()

    def _get_taxful_total_price(self):
        total_price = sum(l.total_price for l in self.lines)
        return total_price if total_price > Decimal('0.0') else Decimal('0.0')

    def _get_product_count(self):
        return sum(l.quantity for l in self.lines if l.product_id)

    def _get_product_lines(self):
        return [l for l in self._get_processed_lines() if l.type != 4]

    def _get_discount_lines(self):
        return [l for l in self._get_processed_lines() if l.type == 4]

    def _get_total_with_postal_fees(self):
        return self.basket_total_price + (Decimal(settings.HKM_POSTAL_FEES) if not self.is_free_shipping else Decimal("0"))

    def _get_postal_fee(self):
        return settings.HKM_POSTAL_FEES

    def _get_free_shipping(self):
        return bool(self._data.get("free_shipping"))

    lines = property(_get_processed_lines)
    product_lines = property(_get_product_lines)
    discount_lines = property(_get_discount_lines)
    data = property(load)
    _raw_lines = property(_get_data_lines, _set_data_lines)
    basket_total_price = property(_get_taxful_total_price)
    postal_fee = property(_get_postal_fee)
    product_count = property(_get_product_count)
    total_price_with_postal_fees = property(_get_total_with_postal_fees)
    is_free_shipping = property(_get_free_shipping)