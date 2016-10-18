
# -*- coding: utf-8 -*-

import logging
from ordered_model.models import OrderedModel
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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

  user = models.OneToOneField(User, verbose_name=_(u'User'))
  is_admin = models.BooleanField(verbose_name=_(u'Is admin'), default=False)
  language = models.CharField(verbose_name=_(u'Language'), default=LANG_FI,
      choices=LANGUAGE_CHOICES, max_length=4)

  def __unicode__(self):
    return self.user.username


class Collection(BaseModel):
  owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
  title = models.CharField(verbose_name=_(u'Title'), max_length=255)
  description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)

  def __unicode__(self):
    return self.title


def get_image_upload_pathupload_to(instance, filename):
  return 'images/%(username)s/%(collection_title)s_%(collection_id)d/%(filename)s' % {
      'username': instance.collection.owner.username,
      'collection_title': instance.collection.title,
      'collection_id': instance.collection.id,
      'filename': filename,
    }


class Image(OrderedModel, BaseModel):
  order_with_respect_to = 'collection'

  creator = models.ForeignKey(User, verbose_name=_(u'Creator'))
  collection = models.ForeignKey(Collection, verbose_name=_(u'Collection'))
  full_res_url = models.CharField(verbose_name=_(u'Full res URL'), max_length=1024)
  edited_image = models.ImageField(verbose_name=_(u'Edited image'), null=True, blank=True,
      upload_to=get_image_upload_pathupload_to)

  class Meta(OrderedModel.Meta):
    pass


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
