import datetime
import random
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.managers import TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields

CAMPAIGN_CODE_KEYSPACE = "acdefghkmnpqrstvwx123456789"


class CampaignUsageType(object):
    SINGLE_USE = "SINGLE_USE"
    CODELESS = "CODELESS"

    choices = (
        (SINGLE_USE, ("Kertakäyttöinen")),
        (CODELESS, ("Kooditon")),
    )


class CodeUsage(object):
    SINGLE_USE = "SINGLE_USE"
    MULTI_USE = "MULTI_USE"

    choices = ((SINGLE_USE, ("Kertakäyttöinen")), (MULTI_USE, ("Monikäyttöinen")))


class CampaignStatus(object):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"

    choices = ((DISABLED, ("Ei käytössä")), (ENABLED, ("Aktiivinen")))


class CampaignUserGroup(object):
    ALL = "ALL"
    MUSEUM = "MUSEUM"
    NORMAL = "NORMAL"

    choices = (
        (ALL, ("Kaikki")),
        (MUSEUM, ("Kioskikäyttäjät")),
        (NORMAL, ("Normaalikäyttäjät")),
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
            if user.is_anonymous:  # No way to know whether it's used or not
                return False
            return self.campaign_usage.filter(order__user=user).exists()
        # because this mixin is inherited by Campaign AND Code check that SINGLE_USE applies only for Codes
        elif self.usage_type == CampaignUsageType.SINGLE_USE and not issubclass(
            type(self), Campaign
        ):
            return self.campaign_usage.exists()
        else:
            return False


class CampaignQuerySet(TranslatableQuerySet):
    def for_user_group(self, is_museum_user=False):
        if is_museum_user:
            return self.filter(
                user_group__in=[CampaignUserGroup.MUSEUM, CampaignUserGroup.ALL]
            )
        else:
            return self.filter(
                user_group__in=[CampaignUserGroup.NORMAL, CampaignUserGroup.ALL]
            )


class Campaign(TranslatableModel, _UsageMixin):
    identifier = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    status = models.CharField(
        default=CampaignStatus.ENABLED,
        verbose_name=_("Tila"),
        db_index=True,
        max_length=20,
        choices=CampaignStatus.choices,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)

    usable_from = models.DateField(
        null=True, blank=True, verbose_name=_("Alkupäivämäärä")
    )
    usable_to = models.DateField(
        null=True, blank=True, verbose_name=_("Loppupäivämäärä")
    )
    usage_type = models.CharField(
        default=CampaignUsageType.SINGLE_USE,
        max_length=20,
        verbose_name=_("Tyyppi"),
        choices=CampaignUsageType.choices,
    )
    user_group = models.CharField(
        default=CampaignUserGroup.ALL,
        verbose_name=_("Käyttäjäryhmä"),
        max_length=20,
        choices=CampaignUserGroup.choices,
        help_text="Käyttäjäryhmä, jolle tarjous on voimassa",
    )
    module = models.CharField(
        max_length=128, blank=True, verbose_name=_("Kampanjamoduuli")
    )
    mutex_group = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_("Yhteiskäyttöestoryhmä"),
        help_text="Mikäli asetettu, useampaa saman ryhmän kampanjaa ei voi käyttää yhdessä tilauksessa",
    )

    percentage_discount = models.DecimalField(
        decimal_places=2,
        verbose_name=_("Prosentuaalinen alennus"),
        max_digits=10,
        null=True,
        blank=True,
    )
    fixed_discount = models.DecimalField(
        decimal_places=2,
        verbose_name=_("Absoluuttinen alennus (veroton)"),
        max_digits=10,
        null=True,
        blank=True,
    )
    free_shipping = models.BooleanField(default=False, verbose_name=_("Free shipping"))
    translations = TranslatedFields(
        name=models.CharField(max_length=256, blank=True, verbose_name=_("Nimi"))
    )

    objects = CampaignQuerySet.as_manager()

    class Meta:
        verbose_name = _("kampanja")
        verbose_name_plural = _("kampanjat")

    def __str__(self):
        return self.safe_translation_getter(
            "name", default=f"{self._meta.verbose_name} {self.pk}", any_language=False
        )

    def get_discount_value(self, basket_lines):
        total_price = sum(line.total_price for line in basket_lines if line.type != 4)
        p_discount = 0
        f_discount = 0
        if self.percentage_discount:
            p_discount = (self.percentage_discount / 100) * total_price
        if self.fixed_discount:
            f_discount = self.fixed_discount

        return Decimal(max(p_discount, f_discount) * -1)


class CampaignCode(models.Model, _UsageMixin):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="campaign_codes",
        verbose_name=("Kampanja"),
    )
    code = models.CharField(max_length=40, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    use_type = models.CharField(
        max_length=20,
        default=CodeUsage.SINGLE_USE,
        verbose_name=_("Käyttö"),
        db_index=True,
        choices=CodeUsage.choices,
    )
    status = models.CharField(
        max_length=20,
        default=CampaignStatus.ENABLED,
        verbose_name=_("Tila"),
        db_index=True,
        choices=CampaignStatus.choices,
    )

    class Meta:
        verbose_name = _("kampanjakoodi")
        verbose_name_plural = _("kampanjakoodit")

    def generate_code(self, length=10, prefix="", unique=True):
        while True:
            self.code = (
                prefix
                + "".join(
                    random.choice(CAMPAIGN_CODE_KEYSPACE) for x in range(length)
                ).upper()
            )
            if unique and CampaignCode.objects.filter(code=self.code).exists():
                continue
            break

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.code
