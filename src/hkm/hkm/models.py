
# -*- coding: utf-8 -*-

import logging
from ordered_model.models import OrderedModel
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

LOG = logging.getLogger(__name__)


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
    return self.filter(owner=user)

  def user_can_view(self, user):
    is_own = models.Q(owner=user)
    is_public = models.Q(public=True)
    return self.filter(is_own|is_public)


class Collection(BaseModel):
  owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
  title = models.CharField(verbose_name=_(u'Title'), max_length=255)
  description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)
  public = models.BooleanField(verbose_name=_(u'Public'), default=False)
  show_in_landing_page = models.BooleanField(verbose_name=_(u'Public'), default=False)

  objects = CollectionQuerySet.as_manager()

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


def get_image_upload_pathupload_to(instance, filename):
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
      upload_to=get_image_upload_pathupload_to)

  class Meta(OrderedModel.Meta):
    pass


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
  if created:
    profile = UserProfile(user=instance)
    profile.save()


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
