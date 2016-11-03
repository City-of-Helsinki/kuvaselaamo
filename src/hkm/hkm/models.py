
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
    is_public = models.Q(public=True)
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
  public = models.BooleanField(verbose_name=_(u'Public'), default=False)
  show_in_landing_page = models.BooleanField(verbose_name=_(u'Public'), default=False)
  collection_type = models.CharField(verbose_name=_(u'Type'), max_length=255, choices=TYPE_CHOICES,
    default=TYPE_NORMAL)

  objects = CollectionQuerySet.as_manager()

  def clean(self):
    print "----------------"
    if self.collection_type == Collection.TYPE_FAVORITE:
      favorite_collections = Collection.objects.filter(owner=self.owner, collection_type=Collection.TYPE_FAVORITE)
      if self.id:
        favorite_collections = favorite_collections.exclude(id=self.id)
      if favorite_collections.exists():
        raise ValidationError('Only one Favorite collection per user is allowed')


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


def get_image_upload_path(instance, filename):
  return 'images/%(username)s/%(collection_title)s_%(collection_id)d/%(filename)s' % {
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
  edited_image = models.ImageField(verbose_name=_(u'Edited image'), null=True, blank=True,
      upload_to=get_image_upload_path)

  class Meta(OrderedModel.Meta):
    pass

  def get_details(self):
    cache_key = '%s-details' % self.record_id
    data = DEFAULT_CACHE.get(cache_key, None)
    if data == None:
      data = FINNA.get_record(self.record_id)
      DEFAULT_CACHE.set(cache_key, data, 60 * 15)
    else:
      LOG.debug('Got record details from cache', extra={'data': {'record_id': self.record_id}})
    return data

  def get_full_res_image_absolute_url(self):
    if self.edited_image:
      return u'%s/%s' % (settings.MY_DOMAIN, self.edited_image.url)
    else:
      record_data = self.get_details()
      record_url = record_data['records'][0]['rawData']['thumbnail']
      cache_key = '%s-record-preview-url' % record_url
      full_res_url = DEFAULT_CACHE.get(cache_key, None)
      if full_res_url == None:
        full_res_url = HKM.get_full_res_image_url(record_data['records'][0]['rawData']['thumbnail'])
        DEFAULT_CACHE.set(cache_key, full_res_url, 60 * 15)
      else:
        LOG.debug('Got record full res url from cache', extra={'data': {'full_res_url': repr(full_res_url)}})
      return full_res_url


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
  if created:
    profile = UserProfile(user=instance)
    profile.save()


class Product(BaseModel):
  name = models.CharField(verbose_name=_(u'Name'), max_length=255)
  description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)
  prize = models.DecimalField(verbose_name=_(u'Prize'), decimal_places=2, max_digits=10)

  class Meta:
    abstract = True

  def __unicode__(self):
    return self.name


class PrintProduct(Product):
  width = models.IntegerField(verbose_name=_(u'Width'))
  height = models.IntegerField(verbose_name=_(u'Height'))
  paper_quality = models.CharField(verbose_name=_(u'Paper quality'), max_length=255)


class ProductOrder(BaseModel):
  # Anonymous users can order aswell, so we need contact and shipping information directly
  # to order model
  user = models.ForeignKey(User, verbose_name=_(u'User'), null=True, blank=True)
  first_name = models.CharField(verbose_name=_(u'First name'), max_length=255)
  last_name = models.CharField(verbose_name=_(u'Last name'), max_length=255)
  email = models.EmailField(max_length=255, verbose_name=_(u'Email'))
  phone = PhoneNumberField(verbose_name=_(u'Phone number'))
  street_address = models.CharField(verbose_name=_(u'Street adress'), max_length=1024)
  postal_code = models.IntegerField(verbose_name=_(u'Postal code'))
  city = models.CharField(verbose_name=_(u'City'), max_length=255)

  # generic relation to any product sub type. This is stored as a reference,
  # but all information regarding the order MUST be stored in directly in this model
  content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')

  # Order must always specify a URL where the orinting service can download the desired image
  # This can be either as direct URL to HKM image server hoting the original image OR URL to
  # kuvaselaamo server to the cropped image
  image_url = models.CharField(verbose_name=_(u'Image URL'), max_length=2048)
  # If this order is made from Record in collection, the Record is saved for statistics purposes
  record = models.ForeignKey(Record, verbose_name=_(u'Record'), null=True, blank=True)

  # Prize and amount information as they were at the time order was made
  # NOTE: Product prizing might vary so these need to be freezed here
  amount = models.IntegerField(verbose_name=_(u'Amount'), default=1)
  unit_prize = models.DecimalField(verbose_name=_(u'Unit prize'), decimal_places=2, max_digits=10)
  total_prize = models.DecimalField(verbose_name=_(u'Total prize'), decimal_places=2, max_digits=10)

  # Timestamp for when users has confimed the order in kuvaselaamo
  datetime_confirmed = models.DateTimeField(verbose_name=_(u'Confirmed'), null=True, blank=True)
  # Timestamps and stateinformation about hte checkout and pyament flow
  datetime_checkout_started = models.DateTimeField(verbose_name=_(u'Checkout started'), null=True, blank=True)
  datetime_checkout_ended = models.DateTimeField(verbose_name=_(u'Checkout ended'), null=True, blank=True)
  is_checkout_successful = models.NullBooleanField(verbose_name=_(u'Checkout succesful'), null=True, blank=True)
  # Timestamps and state information about the actual product order from print
  datetime_order_started = models.DateTimeField(verbose_name=_(u'Order started'), null=True, blank=True)
  datetime_order_ended = models.DateTimeField(verbose_name=_(u'Order ended'), null=True, blank=True)
  is_order_successful = models.NullBooleanField(verbose_name=_(u'Order succesful'), null=True, blank=True)

  def __unicode__(self):
    return 


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
