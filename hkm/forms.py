# -*- coding: utf-8 -*-

import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from hkm.models.campaigns import CampaignCode
from hkm.models.models import (
    Collection,
    Feedback,
    ProductOrder,
    ProductOrderCollection,
    Showcase,
)

LOG = logging.getLogger(__name__)


class CollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        if not self.user.is_authenticated() or not self.user.profile.is_admin:
            del self.fields["show_in_landing_page"]
            del self.fields["is_featured"]

    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "is_public",
            "show_in_landing_page",
            "is_featured",
        ]


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        commit = kwargs.get("commit", True)
        kwargs["commit"] = False
        feedback = super().save(*args, **kwargs)
        feedback.user = self.user
        if commit:
            feedback.save()
        return feedback

    class Meta:
        model = Feedback
        fields = ["content", "full_name", "email"]


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ["amount"]


class OrderContactInformationForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "street_address",
            "postal_code",
            "city",
        ]


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].required = True

    class Meta:
        model = User
        fields = ["username", "email"]


class ProductOrderCollectionForm(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput(attrs={"value": "checkout"}))
    orderer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Orderer's name"),
    )

    class Meta:
        model = ProductOrderCollection
        fields = ["orderer_name"]


class GenerateCampaignCodesActionForm(forms.Form):
    code_prefix = forms.CharField(
        required=False,
        widget=forms.TextInput,
    )
    code_length = forms.CharField(
        required=False,
        widget=forms.TextInput,
    )
    amount = forms.IntegerField(
        required=False,
    )

    def form_action(self, campaign):
        for i in range(0, self.cleaned_data["amount"]):
            code = CampaignCode(campaign=campaign)
            code.generate_code(
                length=self.cleaned_data["code_length"],
                prefix=self.cleaned_data["code_prefix"],
            )
            code.save()

    # def save(self, campaign):
    #     try:
    #         account, action = self.form_action(account, user)
    #     except errors.Error as e:
    #         error_message = str(e)
    #         self.add_error(None, error_message)
    #         raise
    #
    #     return account, action


class ShowcaseForm(forms.ModelForm):
    class Meta:
        model = Showcase
        fields = ["title", "albums", "show_on_home_page"]

    def clean(self):
        albums = self.cleaned_data.get("albums")

        if albums:
            if albums.count() > 3:
                raise ValidationError(_("Max amount of albums is three"))
        return self.cleaned_data
