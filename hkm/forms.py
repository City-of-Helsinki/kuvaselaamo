# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from hkm.models.models import Collection, Feedback, ProductOrder, ProductOrderCollection

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
        fields = ['title', 'description', 'is_public',
                  'show_in_landing_page', 'is_featured']


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


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['amount']


class OrderContactInformationForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'street_address', 'postal_code', 'city']


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email']


class ProductOrderCollectionForm(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'checkout'}))
    orderer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_(u"Orderer's name"))

    class Meta:
        model = ProductOrderCollection
        fields = ['orderer_name']
