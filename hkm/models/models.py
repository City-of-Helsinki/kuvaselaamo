# -*- coding: utf-8 -*-

import datetime
import json
import logging
import hmac
import hashlib

from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel
from parler.models import TranslatableModel, TranslatedFields
from phonenumber_field.modelfields import PhoneNumberField

from hkm.finna import DEFAULT_CLIENT as FINNA
from hkm.models.campaigns import Campaign, CampaignStatus, CampaignCode, CodeUsage
from hkm.paybyway_client import client as PBW
from hkm.printmotor_client import client as PRINTMOTOR

LOG = logging.getLogger(__name__)
DEFAULT_CACHE = caches['default']


class BaseModel(models.Model):
    created = models.DateTimeField(
        verbose_name=_(u'Created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_(u'Modified'), auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    LANG_FI = 'fi'
    LANG_EN = 'en'
    LANG_SV = 'sv'

    LANGUAGE_CHOICES = (
        (LANG_FI, _(u'Finnish')),
        (LANG_EN, _(u'English')),
        (LANG_SV, _(u'Swedish')),
    )

    user = models.OneToOneField(
        User, verbose_name=_(u'User'), related_name='profile')
    is_admin = models.BooleanField(verbose_name=_(u'Is admin'), default=False)
    language = models.CharField(verbose_name=_(u'Language'), default=LANG_FI,
                                choices=LANGUAGE_CHOICES, max_length=4)
    is_museum = models.BooleanField(verbose_name=_(u'Is museum'), default=False)
    printer_ip = models.GenericIPAddressField(verbose_name=u"Museum printer IP", blank=True, null=True)
    printer_username = models.CharField(verbose_name=u'Printer username', blank=True, null=True, max_length=255)
    printer_password = models.CharField(verbose_name=u'Printer password', blank=True, null=True, max_length=255)
    printer_presets = models.TextField(
        verbose_name=u"Tulostimen presetit",
        default=json.dumps({
            'api-poster-gloss-30x40': 0,
            'api-poster-gloss-40x30': 0,
            'api-poster-30x40': 0,
            'api-poster-40x30': 0,
            'api-poster-50x70': 0,
            'api-poster-70x50': 0,
            'api-poster-gloss-A4-horizontal': 0,
            'api-poster-gloss-A4': 0
        }))

    albums = models.ManyToManyField(
        "Collection",
        help_text=u"List of albums for browsing if user is museum",
        blank=True,
        null=True
    )

    removal_notification_sent = models.DateTimeField(
        verbose_name=_(u'Removal notification sent'), blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    @property
    def get_printer_presets(self):
        return json.loads(self.printer_presets)


class CollectionQuerySet(models.QuerySet):
    def user_can_edit(self, user):
        if user.is_authenticated():
            return self.filter(owner=user)
        return self.none()

    def user_can_view(self, user):
        is_public = models.Q(is_public=True)
        if user.is_authenticated():
            is_own = models.Q(owner=user)
            return self.filter(is_own | is_public)
        return self.filter(is_public)


class Collection(BaseModel):
    TYPE_NORMAL = 'normal'
    TYPE_FAVORITE = 'favorite'

    TYPE_CHOICES = (
        (TYPE_NORMAL, _(u'Normal')),
        (TYPE_FAVORITE, _(u'Favorite')),
    )

    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    title = models.CharField(verbose_name=_(u'Title'), max_length=255)
    description = models.TextField(verbose_name=_(
        u'Description'), null=True, blank=True)
    is_public = models.BooleanField(verbose_name=_(u'Public'), default=False)
    is_featured = models.BooleanField(
        verbose_name=_(u'Featured'), default=False)
    show_in_landing_page = models.BooleanField(
        verbose_name=_(u'Show in landing page'), default=False)
    is_showcaseable = models.BooleanField(verbose_name=_(u'Use in Showcases'), default=False, db_index=True)
    collection_type = models.CharField(verbose_name=_(u'Type'), max_length=255, choices=TYPE_CHOICES,
                                       default=TYPE_NORMAL)

    objects = CollectionQuerySet.as_manager()

    def clean(self):
        if self.collection_type == Collection.TYPE_FAVORITE:
            favorite_collections = Collection.objects.filter(
                owner=self.owner, collection_type=Collection.TYPE_FAVORITE)
            if self.id:
                favorite_collections = favorite_collections.exclude(id=self.id)
            if favorite_collections.exists():
                raise ValidationError(
                    'Only one Favorite collection per user is allowed')

    def save(self, *args, **kwargs):
        if self.show_in_landing_page or self.is_featured or self.is_showcaseable:
            # If collection is shown in landing page, set as featured or showcaseable, it
            # must also be public
            if self.show_in_landing_page:
                # Only one collection in landing page at the time
                Collection.objects.filter(show_in_landing_page=True).update(
                    show_in_landing_page=False)
            self.is_public = True
        return super(Collection, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_next_record(self, record):
        records = self.records.filter(order__gt=record.order)
        if records.exists():
            return records[0]
        return None

    def get_previous_record(self, record):
        records = self.records.filter(order__lt=record.order)
        if records.exists():
            return records.reverse()[0]
        return None


def get_collection_upload_path(instance, filename):
    return '%(username)s/%(collection_title)s_%(collection_id)d/%(filename)s' % {
        'username': instance.collection.owner.username,
        'collection_title': instance.collection.title,
        'collection_id': instance.collection.id,
        'filename': filename,
    }


class Record(OrderedModel, BaseModel):
    order_with_respect_to = 'collection'

    creator = models.ForeignKey(User, verbose_name=_(u'Creator'))
    collection = models.ForeignKey(Collection, verbose_name=_(
        u'Collection'), related_name='records')
    record_id = models.CharField(verbose_name=_(
        u'Finna record ID'), max_length=1024)

    """This is populated by view logic if the Record needs
    its matching Finna data."""
    finna_entry = None

    class Meta(OrderedModel.Meta):
        pass

    def get_details(self):
        cache_key = '%s-details' % self.record_id
        data = DEFAULT_CACHE.get(cache_key, None)
        if data is None:
            finna_results = FINNA.get_record(self.record_id)
            if finna_results and 'records' in finna_results:
                data = finna_results['records'][0]
                DEFAULT_CACHE.set(cache_key, data, 60 * 15)
        else:
            LOG.debug('Got record details from cache', extra={
                      'data': {'record_id': self.record_id}})
        return data

    def get_full_res_image_absolute_url(self):
        record_data = self.get_details()
        if record_data:
            return FINNA.get_full_res_image_url(
                             record_data['id'])
        else:
            LOG.debug('Could not get image from Finna API')

    def get_preview_image_absolute_url(self):
        LOG.debug('Getting web image absolute url', extra={
                  'data': {'finna_id': self.record_id}})

        url = FINNA.get_image_url(self.record_id)

        LOG.debug('Got web image absolute url', extra={'data': {'url': url}})
        return url


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()


class Showcase(BaseModel):
    title = models.CharField(verbose_name=_(u'Showcase title'), max_length=255)
    albums = models.ManyToManyField(Collection, verbose_name=_(u'Albums'), limit_choices_to={'is_showcaseable': True})
    show_on_home_page = models.BooleanField(verbose_name=_(u'Show on Home page'), default=True)

    def __unicode__(self):
        return self.title


class Product(BaseModel):
    name = models.CharField(verbose_name=_(u'Name'), max_length=255)
    description = models.TextField(verbose_name=_(
        u'Description'), null=True, blank=True)
    price = models.DecimalField(verbose_name=_(
        u'Price'), decimal_places=2, max_digits=10, default=1)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class PrintProduct(Product):

    PRODUCT_LAYOUTS_LIST = (
        ('api-poster-gloss-30x40', _(u'api-poster-gloss-30x40')),
        ('api-poster-gloss-40x30', _(u'api-poster-gloss-40x30')),
        ('api-poster-30x40', _(u'api-poster-30x40')),
        ('api-poster-40x30', _(u'api-poster-40x30')),
        ('api-poster-50x70', _(u'api-poster-50x70')),
        ('api-poster-70x50', _(u'api-poster-70x50')),
        ('api-poster-gloss-A4-horizontal', _(u'api-poster-gloss-A4-horizontal')),
        ('api-poster-gloss-A4', _(u'api-poster-gloss-A4')),
    )

    name = models.CharField(choices=PRODUCT_LAYOUTS_LIST,
                            verbose_name=_(u'Name'), max_length=255)
    width = models.IntegerField(verbose_name=_(u'Width'))
    height = models.IntegerField(verbose_name=_(u'Height'))
    paper_quality = models.CharField(
        verbose_name=_(u'Paper quality'), max_length=255)
    is_museum_only = models.BooleanField(default=False, verbose_name=_(u"Museum purchase only"))




class ProductOrderQuerySet(models.QuerySet):
    def for_user(self, user, session_orderid):
        if user.is_authenticated():
            return self.filter(models.Q(user=user) | models.Q(order_hash=session_orderid))
        else:
            return self.filter(order_hash=session_orderid)


class ProductOrder(BaseModel):

    # Anonymous users can order aswell, so we need contact and shipping information directly
    # to order model. Orders are associated to anynymous users via session
    user = models.ForeignKey(User, verbose_name=_(
        u'User'), null=True, blank=True)
    session = models.CharField(verbose_name=_(u'Session'), max_length=255)
    first_name = models.CharField(verbose_name=_(
        u'First name'), max_length=255, null=True, blank=False)
    last_name = models.CharField(verbose_name=_(
        u'Last name'), max_length=255, null=True, blank=False)
    email = models.EmailField(max_length=255, verbose_name=_(
        u'Email'), null=True, blank=False)
    phone = PhoneNumberField(verbose_name=_(
        u'Phone number'), null=True, blank=False)
    street_address = models.CharField(verbose_name=_(
        u'Street adress'), max_length=1024, null=True, blank=False)
    postal_code = models.CharField(
        verbose_name=_(u'Postal code'), max_length=64, null=True, blank=False)
    city = models.CharField(verbose_name=_(
        u'City'), max_length=255, null=True, blank=False)

    # generic relation to any product sub type. This is stored as a reference,
    # but all information regarding the order MUST be stored in directly in
    # this model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Image is cropped just in time order is confirmed, until then crop
    # options are stored here
    record_finna_id = models.CharField(verbose_name=_(
        u'Finna record ID'), max_length=1024, null=True, blank=True)
    crop_x = models.FloatField(verbose_name=_(
        'Crop x coordinate from left'), null=True, blank=True)
    crop_y = models.FloatField(verbose_name=_(
        'Crop y coordinate from top'), null=True, blank=True)
    crop_width = models.FloatField(
        verbose_name=_('Crop width'), null=True, blank=True)
    crop_height = models.FloatField(
        verbose_name=_('Crop height'), null=True, blank=True)
    original_width = models.FloatField(verbose_name=_(
        'Original image width'), null=True, blank=True)
    original_height = models.FloatField(verbose_name=_(
        'Original image height'), null=True, blank=True)
    fullimg_original_width = models.FloatField(verbose_name=_(
        'Full res original image width'), null=True, blank=True)
    fullimg_original_height = models.FloatField(verbose_name=_(
        'Full res original image height'), null=True, blank=True)

    # Order must always specify a URL where the printing service can download the desired image
    # This can be either as direct URL to HKM image server holding the original image OR URL to
    # kuvaselaamo server to the cropped image
    image_url = models.CharField(verbose_name=_(
        u'Image URL'), max_length=2048, null=True, blank=True)
    crop_image_url = models.CharField(verbose_name=_(
        u'Cropped Image URL'), max_length=2048, null=True, blank=True)
    # If this order is made from Record in collection, the Record is saved for
    # statistics purposes
    record = models.ForeignKey(Record, verbose_name=_(
        u'Record'), null=True, blank=True)

    form_phase = models.IntegerField(
        verbose_name=_(u'Order form phase'), default=1)
    order_hash = models.CharField(verbose_name=_(
        u'Randomized order identifier phrase'), max_length=1024, null=True, blank=True, unique=True)
    product_type = models.ForeignKey(PrintProduct, verbose_name=_(
        u'Product type'), null=True, blank=True)
    product_name = models.CharField(verbose_name=_(
        u'Product Name'), max_length=1024, null=True, blank=True)
    # Price and amount information as they were at the time order was made
    # NOTE: Product prizing might vary so these need to be freezed here
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_(u'Amount'), default=1)
    postal_fees = models.DecimalField(verbose_name=_(
        u'Shipping fees'), decimal_places=2, max_digits=10, null=False, blank=False, default=settings.HKM_POSTAL_FEES)
    unit_price = models.DecimalField(verbose_name=_(
        u'Unit price'), decimal_places=2, max_digits=10, null=True, blank=True)
    total_price = models.DecimalField(verbose_name=_(
        u'Total price'), decimal_places=2, max_digits=10, null=True, blank=True)
    total_price_with_postage = models.DecimalField(verbose_name=_(
        u'Total price with postage'), decimal_places=2, max_digits=10, null=True, blank=True)

    # Timestamp for when users has confimed the order in kuvaselaamo
    datetime_confirmed = models.DateTimeField(
        verbose_name=_(u'Confirmed'), null=True, blank=True)

    # Timestamps and state information about payment and checkout
    datetime_checkout_started = models.DateTimeField(
        verbose_name=_(u'Checkout started'), null=True, blank=True)
    datetime_checkout_ended = models.DateTimeField(
        verbose_name=_(u'Checkout ended'), null=True, blank=True)
    is_checkout_successful = models.NullBooleanField(
        verbose_name=_(u'Checkout successful'), null=True, blank=True)

    # Timestamps and state information about payment actually being processed
    datetime_payment_processed = models.DateTimeField(
        verbose_name=_(u'Payment processed at'), null=True, blank=True)
    is_payment_successful = models.NullBooleanField(
        verbose_name=_(u'Payment successful'), null=True, blank=True)

    # Timestamps and state information about the actual product order from
    # print
    datetime_order_started = models.DateTimeField(
        verbose_name=_(u'Order started'), null=True, blank=True)
    datetime_order_ended = models.DateTimeField(
        verbose_name=_(u'Order ended'), null=True, blank=True)
    is_order_successful = models.NullBooleanField(
        verbose_name=_(u'Order successful'), null=True, blank=True)

    # A product order may belong to a collection of orders (multiple prints ordered at once)
    order = models.ForeignKey('ProductOrderCollection', blank=True, null=True, related_name="product_orders")

    objects = ProductOrderQuerySet.as_manager()

    # quick method for canceling payments. not used currently - only works when
    # payments are authorized but not settled (ie not billed)
    def cancel_payment(self):
        cancellation = PBW.cancel(self.order_hash)
        LOG.debug(cancellation)
        if not cancellation:
            LOG.error('ORDER CANCELLATION ERROR ', extra={
                      'data': {'order_hash': self.order_hash}})

        if cancellation['result'] == 0:
            LOG.debug('ORDER CANCELLATION SUCCESSFUL ', extra={
                      'data': {'order_hash': self.order_hash}})
        else:
            LOG.error('ORDER CANCELLATION ERROR ', extra={
                      'data': {'order_hash': self.order_hash}})
        return True

    def save(self, *args, **kwargs):
        if not self.order_hash:
            self.order_hash = get_random_string(20)
        return super(ProductOrder, self).save(*args, **kwargs)

    @classmethod
    def delete_old_data(self, date):
        return self.objects.filter(user__isnull=True, modified__lte=date).delete()

    def __unicode__(self):
        return self.order_hash


class Feedback(BaseModel):
    user = models.ForeignKey(User, verbose_name=_(
        u'User'), null=True, blank=True)
    record_id = models.CharField(verbose_name=_(
        u'Finna record ID'), max_length=1024, null=True, blank=True)
    full_name = models.CharField(verbose_name=_(
        u'Name'), max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, verbose_name=_(
        u'Email'), null=True, blank=True)
    content = models.TextField(verbose_name=_(u'Content'))
    is_notification_sent = models.BooleanField(
        verbose_name=_(u'Notification sent'), default=False)
    sent_from = models.CharField(verbose_name=_(u"Sent from"), max_length=500, null=True, blank=True)

    @classmethod
    def delete_old_data(self, date):
        return self.objects.filter(user__isnull=True, modified__lte=date).delete()


def get_tmp_upload_path(instance, filename):
    return 'tmp/%s' % filename


class TmpImage(BaseModel):
    creator = models.ForeignKey(User, verbose_name=_(
        u'Creator'), blank=True, null=True)
    record_id = models.CharField(verbose_name=_(
        u'Finna record ID'), max_length=1024)
    record_title = models.CharField(verbose_name=_(u'Title'), max_length=1024)
    edited_image = models.ImageField(verbose_name=_(
        u'Edited image'), upload_to=get_tmp_upload_path)

    @classmethod
    def delete_old_data(self, date):
        return self.objects.filter(modified__lte=date, creator__isnull=True).delete()

    def __unicode__(self):
        return self.record_title


class PageContent(BaseModel, TranslatableModel):
    name = models.CharField(
        verbose_name=_(u'Name'),
        max_length=255,
    )
    identifier = models.CharField(
        verbose_name=_(u'Identifier'),
        max_length=255,
        unique=True
    )
    translations = TranslatedFields(
        title=models.CharField(
            verbose_name=_(u"Title"),
            max_length=255
        ),
        content=models.TextField(
            verbose_name=_(u"Content")
        )
    )

    def __unicode__(self):
        return self.name


class ProductOrderDiscount(models.Model):
    # A log of used discounts
    campaign = models.ForeignKey(Campaign)
    order = models.ForeignKey('ProductOrderCollection')
    code_used = models.CharField(max_length=255, verbose_name=_(u'Used discount code'), null=True)
    discounted_value = models.DecimalField(max_digits=6, decimal_places=2)


class ProductOrderCollection(models.Model):
    # A bundle of ProductOrder's for in museum purchases.
    orderer_name = models.CharField(verbose_name=_(u'Orderer\'s name'), max_length=255)
    total_price = models.DecimalField(verbose_name=_(u'Total order price'), max_digits=6, decimal_places=2)
    sent_to_print = models.BooleanField(default=False, verbose_name=_(u'Sent to printer'))

    is_checkout_successful = models.NullBooleanField(
        verbose_name=_(u'Checkout successful'), null=True, blank=True)
    is_payment_successful = models.NullBooleanField(
        verbose_name=_(u'Payment successful'), null=True, blank=True)

    is_order_successful = models.NullBooleanField(
        verbose_name=_(u'Order successful'), null=True, blank=True)

    order_hash = models.CharField(verbose_name=_(
        u'Randomized order collection identifier phrase'), max_length=1024, null=True, blank=True, unique=True)

    def __unicode__(self):
        return "%s - order" % self.orderer_name

    def save(self, *args, **kwargs):
        if not self.order_hash:
            self.order_hash = get_random_string(20)
        return super(ProductOrderCollection, self).save(*args, **kwargs)

    @property
    def is_zero_price(self):
        return self.total_price == Decimal(0)

    def add_discount(self, campaign, code=None, discount_value=0):
        if campaign.is_applicable_today():
            ProductOrderDiscount.objects.create(
                order=self,
                campaign=campaign,
                discounted_value=discount_value,
                code_used=code
            )
            if code:
                code_object = CampaignCode.objects.get(
                    code=code,
                    campaign=campaign
                )
                if code_object.use_type == CodeUsage.SINGLE_USE:
                    code_object.status = CampaignStatus.DISABLED
                    code_object.save(update_fields=['status'])

    def checkout(self):
        checkout_request = PBW.post(self.order_hash, int(
            self.total_price * 100))  # api requires sum in cents
        LOG.debug(checkout_request)
        token = checkout_request.get('token', None)
        # TODO better error logs && datetime_checkout_redirected if success
        if token:
            redirect_url = settings.HKM_PBW_API_ENDPOINT + '/token/%s' % token
            return redirect_url
        return None

    def authcode_valid(self, result):
        SECRET_KEY = settings.HKM_PBW_SECRET_KEY
        received_authcode = result.get('authcode', None)
        if not received_authcode:
            return False

        settled = result.get('settled', None)
        incident_id = result.get('incident_id', None)
        return_code = result.get('return_code', None)

        msg = '%s|%s' % (return_code, self.order_hash)
        if settled:
            msg = '%s|%s' % (msg, settled)
        if incident_id:
            msg = '%s|%s' % (msg, incident_id)

        authcode = hmac.new(SECRET_KEY, msg,
                            hashlib.sha256).hexdigest().upper()
        LOG.debug('COMPARING AUTHCODES', extra={
                    'data': {'order_hash': self.order_hash,
                    'received authcode': received_authcode,
                    'calculated authcode': authcode}})
        return authcode == received_authcode

    def send_order_to_printmotor_and_inform(self):
        """
        Sends order to Printmotor and sets is_order_successful field to True or False
        based on response from Printmotor. Also sends email to customer on successful
        print order request. Returns boolean value which tells if print order request
        was successful or not.
        """

        LOG.debug('sending to Printmotor')
        datetime_order_started = datetime.datetime.now()
        LOG.debug('PRINT ORDER ATTEMPT STARTED AT: ', extra={'data': {
                  'order_hash': self.order_hash, 'time': str(datetime_order_started)}})

        printOrder = PRINTMOTOR.post(self)

        datetime_order_ended = timezone.now()
        self.product_orders.update(datetime_order_ended=datetime_order_ended)
        if printOrder:
            LOG.debug('PRINT ORDER ATTEMPT ENDED AT: ', extra={'data': {
                      'order_hash': self.order_hash, 'time': str(datetime_order_ended)}})
            if printOrder == 200:
                LOG.debug('Successfully sent order to printmotor')
                self.is_order_successful = True
                self.send_mail('print')
            elif printOrder == 400:
                LOG.error(
                    'Bad request to Printmotor, check payload', extra={'data': {
                        'order_hash': self.order_hash, 'time': str(datetime_order_ended)}})
                self.is_order_successful = False
            elif printOrder == 401:
                LOG.error(
                    'Unauthorized @ Printmotor, check headers', extra={'data': {
                        'order_hash': self.order_hash, 'time': str(datetime_order_ended)}})
                self.is_order_successful = False
            elif printOrder == 500:
                LOG.error(
                    'Printmotor server error, maybe image URL is invalid', extra={'data': {
                        'order_hash': self.order_hash, 'time': str(datetime_order_ended)}})
                self.is_order_successful = False
            else:
                LOG.error(
                    'Unknown status code from Printmotor', extra={'data': {
                        'order_hash': self.order_hash, 'time': str(datetime_order_ended),
                        'status_code': printOrder}})
                self.is_order_successful = False
        else:
            LOG.error('Failed to communicate with Printmotor API', extra={'data': {
                      'order_hash': self.order_hash, 'time': str(datetime_order_ended)}})
            self.is_order_successful = False

        return self.is_order_successful

    def handle_zero_price_confirmation(self):

        # Process only if total price is 0
        if not self.is_zero_price:
            return

        datetime_checkout_ended = timezone.now()
        self.product_orders.update(datetime_checkout_ended=datetime_checkout_ended)
        LOG.debug('ZERO PRICE CHECKOUT ENDED AT: ', extra={'data': {
                'order_hash': self.order_hash,
                'time': str(datetime_checkout_ended)}})

        if not self.is_checkout_successful:
            LOG.debug('ZERO PRICE CHECKOUT SUCCESSFUL ', extra={
                      'data': {'order_hash': self.order_hash}})
            self.send_mail('checkout')
            self.is_checkout_successful = True

        # If payment has not yet been marked as successfully processed,
        # Mark it as such and try to send order details to Printing
        # Agency
        if not self.is_payment_successful:
            self.is_payment_successful = True
            LOG.debug('ZERO PRICE PAYMENT SETTLED SUCCESSFULLY ', extra={
                      'data': {'order_hash': self.order_hash}})

        # If order has not yet been marked as successfully sent, send it to PRINTMOTOR
        if not self.is_order_successful:
            self.send_order_to_printmotor_and_inform()
        self.save()

    def handle_confirmation(self, result, force=False):

        if not force:
            if self.is_checkout_successful == False:
                LOG.error('ATTEMPT TO REHANDLE UNSUCCESSFUL CHECKOUT!', extra={'data': {
                          'order_hash': self.order_hash}})
                return
        datetime_checkout_ended = timezone.now()
        self.product_orders.update(datetime_checkout_ended=datetime_checkout_ended)
        LOG.debug('CHECKOUT ENDED AT: ', extra={'data': {
                'order_hash': self.order_hash,
                'time': str(datetime_checkout_ended)}})

        # if return code for checkout is 0 (SUCCESS)
        if result['return_code'] == '0':
            # if order not yet marked as successful,
            # send order confirmation mail to customer and mark checkout as
            # successful
            if not self.is_checkout_successful:
                LOG.debug('CHECKOUT SUCCESSFUL ', extra={
                          'data': {'order_hash': self.order_hash}})
                self.send_mail('checkout')
                self.is_checkout_successful = True

            # If payment has been successfully processed
            if result['settled'] == '1':

                # If payment has not yet been marked as successfully processed,
                # Mark it as such and try to send order details to Printing
                # Agency
                if not self.is_payment_successful:
                    self.is_payment_successful = True
                    LOG.debug('PAYMENT SETTLED SUCCESSFULLY ', extra={
                              'data': {'order_hash': self.order_hash}})

                # If order has not yet been marked as successfully sent, send it to Printmotor
                if not self.is_order_successful:
                    self.send_order_to_printmotor_and_inform()

        else:
            self.is_checkout_successful = False
            LOG.error('CHECKOUT _NOT_ SUCCESSFUL ', extra={
                      'data': {'order_hash': self.order_hash}})

        self.save()

    def send_mail(self, phase):
        if not phase:
            return False

        if phase == 'checkout':
            subject = 'Helsinkikuvia.fi - tilausvahvistus'
            message = 'Hei! Kiitos tilauksestasi. Saat vielä toisen viestin, kun tilaus lähtee painoon.\n\nHelsinkikuvia.fi – helsinkiläisten kuva-aarre verkossa'

        elif phase == 'print':
            subject = 'Helsinkikuvia.fi - tilaus toimitettu painoon'
            message = 'Hei! Tilauksesi on onnistuneesti toimitettu painotalo Printmotorille. Valmis tilaus lähetetään Matkahuollon lähipakettina viimeistään kolmantena arkipäivänä tästä päivästä lukien. Tilaukseen liittyvät yhteydenotot sähköpostitse: support@printmotor.io (mainitse viestissä, että tilaus on tehty Helsinkikuvia.fi-palvelussa).\n\n Helsinkikuvia.fi – helsinkiläisten kuva-aarre verkossa'

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.customer_email])
        return True

    @property
    def customer_email(self):
        return self.product_orders.first().email