from django.core.exceptions import ObjectDoesNotExist

from hkm.models.campaigns import CampaignStatus, Campaign
from hkm.models.models import ProductOrderCollection


class OrderCreator(object):

    def validate_basket(self, basket):
        # For now validate that discounts are still valid
        for line in basket.discount_lines:
            campaign = Campaign.objects.get(pk=line.campaign_id)
            if not campaign.is_applicable_today():
                return False
            if line.code and not campaign.campaign_codes.filter(code=line.code,
                                                                status=CampaignStatus.ENABLED).exists():
                return False
        return True

    def create_order_from_basket(self, basket):
        try:
            order_collection = ProductOrderCollection.objects.get(pk=basket.data.get('order_collection'))
            order_collection.total_price = basket.total_price_with_postal_fees
        except ObjectDoesNotExist:
            order_collection = ProductOrderCollection(total_price=basket.total_price_with_postal_fees)
            order_collection.save()

        for line in basket.lines:
            if line.type == 1 and line.order:
                # a product line
                line.order.order = order_collection
                line.order.amount = line.quantity
                line.order.total_price = line.total_price
                line.order.save()
            if line.type == 4:
                # a discount line
                campaign = Campaign.objects.get(pk=line.campaign_id)
                order_collection.add_discount(campaign=campaign, code=line.code, discount_value=line.discount_value)
        basket.data['order_collection'] = order_collection.pk
        basket.save()
        order_collection.save()
        return order_collection
