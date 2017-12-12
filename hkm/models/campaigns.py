# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields

import datetime
import random

CAMPAIGN_CODE_KEYSPACE = "acdefghkmnpqrstvwx123456789"


class CampaignUsageType(object):
    SINGLE_USE = "SINGLE_USE"
    CODELESS = "CODELESS"

    choices = (
        (SINGLE_USE, (u"Kertakäyttöinen")),
        (CODELESS, (u"Kooditon")),
    )


class CampaignStatus(object):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"

    choices = (
        (DISABLED, (u"Ei käytössä")),
        (ENABLED, (u"Aktiivinen"))
    )


class _UsageMixin(object):
    def is_applicable_in(self, dt):
        if not self.usable_from or dt >= self.usable_from:
            if not self.usable_to or dt <= self.usable_to:
                return True
        return False

    def is_applicable_today(self):
        return self.is_applicable_in(datetime.datetime.now().date())

    def is_used(self, user=None):
        if user and self.usage_type == CampaignUsageType.SINGLE_USE_PER_USER:
            if user.is_anonymous():  # No way to know whether it's used or not
                return False
            return self.campaign_usage.filter(order__user=user).exists()
        # because this mixin is inherited by Campaign AND Code check that SINGLE_USE applies only for Codes
        elif self.usage_type == CampaignUsageType.SINGLE_USE and not issubclass(type(self), Campaign):
            return self.campaign_usage.exists()
        else:
            return False


class Campaign(TranslatableModel, _UsageMixin):
    identifier = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True
    )
    status = models.CharField(
        default=CampaignStatus.ENABLED,
        verbose_name=_(u"Tila"),
        db_index=True,
        max_length=20,
        choices=CampaignStatus.choices
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    usable_from = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u'Alkupäivämäärä')
    )
    usable_to = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u'Loppupäivämäärä')
    )
    usage_type = models.CharField(
        default=CampaignUsageType.SINGLE_USE,
        max_length=20,
        verbose_name=_(u"Tyyppi"),
        choices=CampaignUsageType.choices
    )
    module = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_(u"Kampanjamoduuli")
    )
    mutex_group = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_(u"Yhteiskäyttöestoryhmä"),
        help_text=u"Mikäli asetettu, useampaa saman ryhmän kampanjaa ei voi käyttää yhdessä tilauksessa"
    )

    percentage_discount = models.DecimalField(
        decimal_places=2,
        verbose_name=_(u"Prosentuaalinen alennus"),
        max_digits=10,
        null=True,
        blank=True,
    )
    fixed_discount = models.DecimalField(
        decimal_places=2,
        verbose_name=_(u"Absoluuttinen alennus (veroton)"),
        max_digits=10,
        null=True,
        blank=True,
    )
    free_shipping = models.BooleanField(default=False, verbose_name=_(u'Free shipping'))
    translations = TranslatedFields(
        name=models.CharField(
            max_length=256,
            blank=True,
            verbose_name=_(u"Nimi")
        )
    )

    class Meta:
        verbose_name = _(u"kampanja")
        verbose_name_plural = _(u"kampanjat")

    def __unicode__(self):
        try:
            return unicode(self.name)
        except:
            return "%s %s" % (unicode(self._meta.verbose_name), self.pk)

    def get_discount_value(self, basket_lines):
        total_price = sum(l.total_price for l in basket_lines if l.type != 4)
        p_discount = 0
        f_discount = 0
        if self.percentage_discount:
            p_discount = (self.percentage_discount / 100) * total_price
        if self.fixed_discount:
            f_discount = self.fixed_discount

        return Decimal(max(p_discount, f_discount) * -1)


class CampaignCode(models.Model, _UsageMixin):
    campaign = models.ForeignKey(Campaign, related_name="campaign_codes", verbose_name=(u"Kampanja"))
    code = models.CharField(max_length=40, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default=CampaignStatus.ENABLED,
        verbose_name=_(u"Tila"),
        db_index=True,
        choices=CampaignStatus.choices
    )

    class Meta:
        verbose_name = _(u"kampanjakoodi")
        verbose_name_plural = _(u"kampanjakoodit")

    def generate_code(self, length=10, prefix="", unique=True):
        while True:
            self.code = prefix + "".join(
                random.choice(CAMPAIGN_CODE_KEYSPACE) for x in xrange(length)
            ).upper()
            if unique and CampaignCode.objects.filter(code=self.code).exists():
                continue
            break

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        return super(CampaignCode, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.code