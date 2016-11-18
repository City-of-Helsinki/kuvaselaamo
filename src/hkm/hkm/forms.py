
# -*- coding: utf-8 -*-

import logging
from django import forms
from hkm.models import Collection, Feedback

LOG = logging.getLogger(__name__)


class CollectionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super(CollectionForm, self).__init__(*args, **kwargs)
    if not self.user.is_authenticated() or not self.user.profile.is_admin:
      del self.fields['show_in_landing_page']
      del self.fields['is_featured']

  class Meta:
    model = Collection
    fields = ['title', 'description', 'is_public', 'show_in_landing_page', 'is_featured']


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
