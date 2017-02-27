
# -*- coding: utf-8 -*-

import logging
from ordered_model.models import OrderedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from hkm.finna import DEFAULT_CLIENT as FINNA
from hkm.hkm_client import DEFAULT_CLIENT as HKM
from hkm import settings

LOG = logging.getLogger(__name__)
DEFAULT_CACHE = caches['default']

class BaseModel(models.Model):
  created = models.DateTimeField(verbose_name=_(u'Created'), auto_now_add=True)
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
    (LANG_SV, _(u'Svedish')),
  )

  user = models.OneToOneField(User, verbose_name=_(u'User'), related_name='profile')
  is_admin = models.BooleanField(verbose_name=_(u'Is admin'), default=False)
  language = models.CharField(verbose_name=_(u'Language'), default=LANG_FI,
      choices=LANGUAGE_CHOICES, max_length=4)

  def __unicode__(self):
    return self.user.username


class CollectionQuerySet(models.QuerySet):
  def user_can_edit(self, user):
    if user.is_authenticated():
      return self.filter(owner=user)
    return self.none()

  def user_can_view(self, user):
    is_public = models.Q(is_public=True)
    if user.is_authenticated():
      is_own = models.Q(owner=user)
      return self.filter(is_own|is_public)
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
  description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)
  is_public = models.BooleanField(verbose_name=_(u'Public'), default=False)
  is_featured = models.BooleanField(verbose_name=_(u'Featured'), default=False)
  show_in_landing_page = models.BooleanField(verbose_name=_(u'Show in landing page'), default=False)
  collection_type = models.CharField(verbose_name=_(u'Type'), max_length=255, choices=TYPE_CHOICES,
    default=TYPE_NORMAL)

  objects = CollectionQuerySet.as_manager()

  def clean(self):
    if self.collection_type == Collection.TYPE_FAVORITE:
      favorite_collections = Collection.objects.filter(owner=self.owner, collection_type=Collection.TYPE_FAVORITE)
      if self.id:
        favorite_collections = favorite_collections.exclude(id=self.id)
      if favorite_collections.exists():
        raise ValidationError('Only one Favorite collection per user is allowed')

  def save(self, *args, **kwargs):
    if self.show_in_landing_page or self.is_featured:
      # If collection is shown in landing page or set as featured, it must also be public
      if self.show_in_landing_page:
        # Only one collection in landing page at the time
        Collection.objects.filter(show_in_landing_page=True).update(show_in_landing_page=False)
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
  collection = models.ForeignKey(Collection, verbose_name=_(u'Collection'), related_name='records')
  record_id = models.CharField(verbose_name=_(u'Finna record ID'), max_length=1024)
  edited_full_res_image = models.ImageField(verbose_name=_(u'Edited full resolution image'), null=True, blank=True,
      upload_to=get_collection_upload_path)
  edited_preview_image = models.ImageField(verbose_name=_(u'Edited preview image'), null=True, blank=True,
      upload_to=get_collection_upload_path)

  class Meta(OrderedModel.Meta):
    pass

  def get_details(self):
    cache_key = '%s-details' % self.record_id
    data = DEFAULT_CACHE.get(cache_key, None)
    if data == None:
      data = FINNA.get_record(self.record_id)
      if data:
        data = data['records'][0]
        DEFAULT_CACHE.set(cache_key, data, 60 * 15)
    else:
      LOG.debug('Got record details from cache', extra={'data': {'record_id': self.record_id}})
    return data

  def get_full_res_image_absolute_url(self):
    if self.edited_full_res_image:
      return u'%s%s' % (settings.MY_DOMAIN, self.edited_full_res_image.url)
    else:
      record_data = self.get_details()
      if record_data:
        record_url = record_data['rawData']['thumbnail']
        cache_key = '%s-record-preview-url' % record_url
        full_res_url = DEFAULT_CACHE.get(cache_key, None)
        if full_res_url == None:
          full_res_url = HKM.get_full_res_image_url(record_data['rawData']['thumbnail'])
          DEFAULT_CACHE.set(cache_key, full_res_url, 60 * 15)
        else:
          LOG.debug('Got record full res url from cache', extra={'data': {'full_res_url': repr(full_res_url)}})
        return full_res_url
      else:
        LOG.debug('Could not get image from Finna API')

  def get_preview_image_absolute_url(self):
    if self.edited_preview_image:
      return u'%s%s' % (settings.MY_DOMAIN, self.edited_preview_image.url)
    else:
      return FINNA.get_image_url(self.record_id)

  def is_favorite(self, user):
    if user.is_authenticated():
      try:
        favorites_collection = Collection.objects.get(owner=user, collection_type=Collection.TYPE_FAVORITE)
      except Collection.DoesNotExist:
        pass
      else:
        return favorites_collection.records.filter(record_id=self.record_id).exists()
    return False


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
  if created:
    profile = UserProfile(user=instance)
    profile.save()


class Product(BaseModel):
  name = models.CharField(verbose_name=_(u'Name'), max_length=255)
  description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)
  price = models.DecimalField(verbose_name=_(u'Price'), decimal_places=2, max_digits=10, default=1)

  class Meta:
    abstract = True

  def __unicode__(self):
    return self.name


class PrintProduct(Product):
  width = models.IntegerField(verbose_name=_(u'Width'))
  height = models.IntegerField(verbose_name=_(u'Height'))
  paper_quality = models.CharField(verbose_name=_(u'Paper quality'), max_length=255)


class ProductOrderQuerySet(models.QuerySet):
  def for_user(self, user, session_key):
    if user.is_authenticated():
      return self.filter(models.Q(user=user)|models.Q(session=session_key))
    else:
      return self.filter(session=session_key)

class ProductOrder(BaseModel):
  # Anonymous users can order aswell, so we need contact and shipping information directly
  # to order model. Orders are associated to anynymous users via session
  user = models.ForeignKey(User, verbose_name=_(u'User'), null=True, blank=True)
  session = models.CharField(verbose_name=_(u'Session'), max_length=255)
  first_name = models.CharField(verbose_name=_(u'First name'), max_length=255, null=True, blank=False)
  last_name = models.CharField(verbose_name=_(u'Last name'), max_length=255, null=True, blank=False)
  email = models.EmailField(max_length=255, verbose_name=_(u'Email'), null=True, blank=False)
  phone = PhoneNumberField(verbose_name=_(u'Phone number'), null=True, blank=False)
  street_address = models.CharField(verbose_name=_(u'Street adress'), max_length=1024, null=True, blank=False)
  postal_code = models.IntegerField(verbose_name=_(u'Postal code'), null=True, blank=False)
  city = models.CharField(verbose_name=_(u'City'), max_length=255, null=True, blank=False)

  # generic relation to any product sub type. This is stored as a reference,
  # but all information regarding the order MUST be stored in directly in this model
  content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
  object_id = models.PositiveIntegerField(null=True, blank=True)
  content_object = GenericForeignKey('content_type', 'object_id')

  # Image is cropped just in time order is confirmed, until then crop options are stored here
  record_finna_id = models.CharField(verbose_name=_(u'Finna record ID'), max_length=1024, null=True, blank=True)
  crop_x = models.FloatField(verbose_name=_('Crop x coordinate from left'), null=True, blank=True)
  crop_y = models.FloatField(verbose_name=_('Crop y coordinate from top'), null=True, blank=True)
  crop_width = models.FloatField(verbose_name=_('Crop width'), null=True, blank=True)
  crop_height = models.FloatField(verbose_name=_('Crop height'), null=True, blank=True)
  original_width = models.FloatField(verbose_name=_('Original image width'), null=True, blank=True)
  original_height = models.FloatField(verbose_name=_('Original image height'), null=True, blank=True)
  fullimg_original_width = models.FloatField(verbose_name=_('Full res original image width'), null=True, blank=True)
  fullimg_original_height = models.FloatField(verbose_name=_('Full res original image height'), null=True, blank=True)

  # Order must always specify a URL where the printing service can download the desired image
  # This can be either as direct URL to HKM image server holding the original image OR URL to
  # kuvaselaamo server to the cropped image
  image_url = models.CharField(verbose_name=_(u'Image URL'), max_length=2048, null=True, blank=True)
  crop_image_url = models.CharField(verbose_name=_(u'Cropped Image URL'), max_length=2048, null=True, blank=True)
  # If this order is made from Record in collection, the Record is saved for statistics purposes
  record = models.ForeignKey(Record, verbose_name=_(u'Record'), null=True, blank=True)

  form_phase = models.IntegerField(verbose_name=_(u'Order form phase'), default=1)
  order_hash = models.CharField(verbose_name=_(u'Randomized order identifier phrase'), max_length=1024, null=True, blank=True)
  product_type = models.ForeignKey(PrintProduct, verbose_name=_(u'Product type'), default=6, blank=True)
  product_name = models.CharField(verbose_name=_(u'Product Name'), max_length=1024, null=True, blank=True)
  # Price and amount information as they were at the time order was made
  # NOTE: Product prizing might vary so these need to be freezed here
  amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_(u'Amount'), default=1)
  unit_price = models.DecimalField(verbose_name=_(u'Unit price'), decimal_places=2, max_digits=10, null=True, blank=True)
  total_price = models.DecimalField(verbose_name=_(u'Total price'), decimal_places=2, max_digits=10, null=True, blank=True)

  # Timestamp for when users has confimed the order in kuvaselaamo
  datetime_confirmed = models.DateTimeField(verbose_name=_(u'Confirmed'), null=True, blank=True)
  
  # Timestamps and state information about payment and checkout
  datetime_checkout_started = models.DateTimeField(verbose_name=_(u'Checkout started'), null=True, blank=True)
  datetime_checkout_ended = models.DateTimeField(verbose_name=_(u'Checkout ended'), null=True, blank=True)
  is_checkout_successful = models.NullBooleanField(verbose_name=_(u'Checkout successful'), null=True, blank=True)
  
  # Timestamps and state information about payment actually being processed
  datetime_payment_processed = models.DateTimeField(verbose_name=_(u'Payment processed at'), null=True, blank=True)
  is_payment_successful = models.NullBooleanField(verbose_name=_(u'Payment successful'), null=True, blank=True)
  
  # Timestamps and state information about the actual product order from print
  datetime_order_started = models.DateTimeField(verbose_name=_(u'Order started'), null=True, blank=True)
  datetime_order_ended = models.DateTimeField(verbose_name=_(u'Order ended'), null=True, blank=True)
  is_order_successful = models.NullBooleanField(verbose_name=_(u'Order successful'), null=True, blank=True)

  objects = ProductOrderQuerySet.as_manager()

  def __unicode__(self):
    return self.session


class Feedback(BaseModel):
  user = models.ForeignKey(User, verbose_name=_(u'User'), null=True, blank=True)
  record_id = models.CharField(verbose_name=_(u'Finna record ID'), max_length=1024, null=True, blank=True)
  full_name = models.CharField(verbose_name=_(u'Name'), max_length=255, null=True, blank=True)
  email = models.EmailField(max_length=255, verbose_name=_(u'Email'), null=True, blank=True)
  content = models.TextField(verbose_name=_(u'Content'))
  is_notification_sent = models.BooleanField(verbose_name=_(u'Notification sent'), default=False)


def get_tmp_upload_path(instance, filename):
  return 'tmp/%s' % filename

class TmpImage(BaseModel):
  creator = models.ForeignKey(User, verbose_name=_(u'Creator'), blank=True, null=True)
  record_id = models.CharField(verbose_name=_(u'Finna record ID'), max_length=1024)
  record_title = models.CharField(verbose_name=_(u'Title'), max_length=1024)
  edited_image = models.ImageField(verbose_name=_(u'Edited image'), upload_to=get_tmp_upload_path)

  def __unicode__(self):
    return self.record_title


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
