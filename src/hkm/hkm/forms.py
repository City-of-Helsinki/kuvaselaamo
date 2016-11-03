
# -*- coding: utf-8 -*-

import logging
from django import forms
from hkm.models import Collection

LOG = logging.getLogger(__name__)


class CollectionForm(forms.ModelForm):
  class Meta:
    model = Collection
    fields = ['title', 'description']


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
