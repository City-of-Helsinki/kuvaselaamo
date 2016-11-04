
# -*- coding: utf-8 -*-

import logging
from django import forms
from hkm.models import Collection, Feedback

LOG = logging.getLogger(__name__)


class CollectionForm(forms.ModelForm):
  class Meta:
    model = Collection
    fields = ['title', 'description']


class FeedbackForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user', None)
    return super(FeedbackForm, self).__init__(*args, **kwargs)

  def save(self, *args, **kwargs):
    commit = kwargs.get('commit', True)
    kwargs['commit'] = False
    feedback = super(FeedbackForm, self).save(*args, **kwargs)
    feedback.user = self.user
    if commit:
      feedback.save()
    return feedback

  class Meta:
    model = Feedback
    fields = ['content', 'full_name', 'email']

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
