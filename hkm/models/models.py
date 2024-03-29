import json
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel
from parler.models import TranslatableModel, TranslatedFields
from phonenumber_field.modelfields import PhoneNumberField

from hkm.finna import DEFAULT_CLIENT as FINNA
from hkm.models.campaigns import Campaign

LOG = logging.getLogger(__name__)
DEFAULT_CACHE = caches["default"]


def _update_removal_notification_sent(sender, user, **kwargs):
    """
    A signal receiver which clears the value of removal_notification_sent of the user logging in.
    """
    user.profile.removal_notification_sent = None
    user.profile.save(update_fields=["removal_notification_sent"])


user_logged_in.connect(_update_removal_notification_sent)


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    LANG_FI = "fi"
    LANG_EN = "en"
    LANG_SV = "sv"

    LANGUAGE_CHOICES = (
        (LANG_FI, _("Finnish")),
        (LANG_EN, _("English")),
        (LANG_SV, _("Swedish")),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="profile"
    )
    is_admin = models.BooleanField(verbose_name=_("Is admin"), default=False)
    language = models.CharField(
        verbose_name=_("Language"),
        default=LANG_FI,
        choices=LANGUAGE_CHOICES,
        max_length=4,
    )
    is_museum = models.BooleanField(verbose_name=_("Is museum"), default=False)
    printer_ip = models.GenericIPAddressField(
        verbose_name="Museum printer IP", blank=True, null=True
    )
    printer_username = models.CharField(
        verbose_name="Printer username", blank=True, null=True, max_length=255
    )
    printer_password = models.CharField(
        verbose_name="Printer password", blank=True, null=True, max_length=255
    )
    printer_presets = models.TextField(
        verbose_name="Tulostimen presetit",
        default=json.dumps(
            {
                "api-poster-gloss-30x40": 0,
                "api-poster-gloss-40x30": 0,
                "api-poster-30x40": 0,
                "api-poster-40x30": 0,
                "api-poster-50x70": 0,
                "api-poster-70x50": 0,
                "api-poster-gloss-A4-horizontal": 0,
                "api-poster-gloss-A4": 0,
            }
        ),
    )

    albums = models.ManyToManyField(
        "Collection",
        help_text="List of albums for browsing if user is museum",
        blank=True,
    )

    removal_notification_sent = models.DateTimeField(
        verbose_name=_("Removal notification sent"), blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    @property
    def get_printer_presets(self):
        return json.loads(self.printer_presets)


class CollectionQuerySet(models.QuerySet):
    def user_can_edit(self, user):
        if user.is_authenticated:
            return self.filter(owner=user)
        return self.none()

    def user_can_view(self, user):
        is_public = models.Q(is_public=True)
        if user.is_authenticated:
            is_own = models.Q(owner=user)
            return self.filter(is_own | is_public)
        return self.filter(is_public)


class Collection(BaseModel):
    TYPE_NORMAL = "normal"
    TYPE_FAVORITE = "favorite"

    TYPE_CHOICES = (
        (TYPE_NORMAL, _("Normal")),
        (TYPE_FAVORITE, _("Favorite")),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Owner"))
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    is_public = models.BooleanField(verbose_name=_("Public"), default=False)
    is_featured = models.BooleanField(verbose_name=_("Featured"), default=False)
    show_in_landing_page = models.BooleanField(
        verbose_name=_("Show in landing page"), default=False
    )
    is_showcaseable = models.BooleanField(
        verbose_name=_("Use in Showcases"), default=False, db_index=True
    )
    collection_type = models.CharField(
        verbose_name=_("Type"),
        max_length=255,
        choices=TYPE_CHOICES,
        default=TYPE_NORMAL,
    )

    objects = CollectionQuerySet.as_manager()

    def clean(self):
        if self.collection_type == Collection.TYPE_FAVORITE:
            favorite_collections = Collection.objects.filter(
                owner=self.owner, collection_type=Collection.TYPE_FAVORITE
            )
            if self.id:
                favorite_collections = favorite_collections.exclude(id=self.id)
            if favorite_collections.exists():
                raise ValidationError(
                    "Only one Favorite collection per user is allowed"
                )

    def save(self, *args, **kwargs):
        if self.show_in_landing_page or self.is_featured or self.is_showcaseable:
            # If collection is shown in landing page, set as featured or showcaseable, it
            # must also be public
            if self.show_in_landing_page:
                # Only one collection in landing page at the time
                Collection.objects.filter(show_in_landing_page=True).update(
                    show_in_landing_page=False
                )
            self.is_public = True
        return super().save(*args, **kwargs)

    def __str__(self):
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


def get_collection_upload_path(instance, filename):
    username = instance.collection.owner.username
    collection_title = instance.collection.title
    collection_id = instance.collection.id
    return f"{username}/{collection_title}_{collection_id:d}/{filename}"


class Record(OrderedModel, BaseModel):
    order_with_respect_to = "collection"

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Creator")
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        verbose_name=_("Collection"),
        related_name="records",
    )
    record_id = models.CharField(verbose_name=_("Finna record ID"), max_length=1024)

    """This is populated by view logic if the Record needs
    its matching Finna data."""
    finna_entry = None

    class Meta(OrderedModel.Meta):
        pass

    def get_details(self):
        cache_key = f"{self.record_id}-details"
        data = DEFAULT_CACHE.get(cache_key, None)
        if data is None:
            finna_results = FINNA.get_record(self.record_id)
            if finna_results and "records" in finna_results:
                data = finna_results["records"][0]
                DEFAULT_CACHE.set(cache_key, data, 60 * 15)
        else:
            LOG.debug(
                "Got record details from cache",
                extra={"data": {"record_id": self.record_id}},
            )
        return data

    def get_full_res_image_absolute_url(self):
        record_data = self.get_details()
        if record_data:
            return FINNA.get_full_res_image_url(record_data)
        else:
            LOG.debug("Could not get image from Finna API")

    def get_preview_image_absolute_url(self):
        LOG.debug(
            "Getting web image absolute url",
            extra={"data": {"finna_id": self.record_id}},
        )

        url = FINNA.get_image_url(self.record_id)

        LOG.debug("Got web image absolute url", extra={"data": {"url": url}})
        return url

    def get_thumbnail_image_absolute_url(self):
        record_data = self.get_details()
        if record_data:
            return FINNA.get_thumbnail_image_url(record_data)
        else:
            LOG.debug("Could not get image from Finna API")


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()


class Showcase(BaseModel):
    title = models.CharField(verbose_name=_("Showcase title"), max_length=255)
    albums = models.ManyToManyField(
        Collection, verbose_name=_("Albums"), limit_choices_to={"is_showcaseable": True}
    )
    show_on_home_page = models.BooleanField(
        verbose_name=_("Show on Home page"), default=True
    )

    def __str__(self):
        return self.title


class Product(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    price = models.DecimalField(
        verbose_name=_("Price"), decimal_places=2, max_digits=10, default=1
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PrintProduct(Product):

    PRODUCT_LAYOUTS_LIST = (
        ("api-poster-gloss-30x40", _("api-poster-gloss-30x40")),
        ("api-poster-gloss-40x30", _("api-poster-gloss-40x30")),
        ("api-poster-30x40", _("api-poster-30x40")),
        ("api-poster-40x30", _("api-poster-40x30")),
        ("api-poster-50x70", _("api-poster-50x70")),
        ("api-poster-70x50", _("api-poster-70x50")),
        ("api-poster-gloss-A4-horizontal", _("api-poster-gloss-A4-horizontal")),
        ("api-poster-gloss-A4", _("api-poster-gloss-A4")),
    )

    name = models.CharField(
        choices=PRODUCT_LAYOUTS_LIST, verbose_name=_("Name"), max_length=255
    )
    width = models.IntegerField(verbose_name=_("Width"))
    height = models.IntegerField(verbose_name=_("Height"))
    paper_quality = models.CharField(verbose_name=_("Paper quality"), max_length=255)
    is_museum_only = models.BooleanField(
        default=False, verbose_name=_("Museum purchase only")
    )


class ProductOrderQuerySet(models.QuerySet):
    def for_user(self, user, session_orderid):
        if user.is_authenticated:
            return self.filter(
                models.Q(user=user) | models.Q(order_hash=session_orderid)
            )
        else:
            return self.filter(order_hash=session_orderid)


class ProductOrder(BaseModel):

    # Anonymous users can order aswell, so we need contact and shipping information directly
    # to order model. Orders are associated to anynymous users via session
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("User"), null=True, blank=True
    )
    session = models.CharField(verbose_name=_("Session"), max_length=255)
    first_name = models.CharField(
        verbose_name=_("First name"), max_length=255, null=True, blank=False
    )
    last_name = models.CharField(
        verbose_name=_("Last name"), max_length=255, null=True, blank=False
    )
    email = models.EmailField(
        max_length=255, verbose_name=_("Email"), null=True, blank=False
    )
    phone = PhoneNumberField(verbose_name=_("Phone number"), null=True, blank=False)
    street_address = models.CharField(
        verbose_name=_("Street adress"), max_length=1024, null=True, blank=False
    )
    postal_code = models.CharField(
        verbose_name=_("Postal code"), max_length=64, null=True, blank=False
    )
    city = models.CharField(
        verbose_name=_("City"), max_length=255, null=True, blank=False
    )

    # generic relation to any product sub type. This is stored as a reference,
    # but all information regarding the order MUST be stored in directly in
    # this model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # Image is cropped just in time order is confirmed, until then crop
    # options are stored here
    record_finna_id = models.CharField(
        verbose_name=_("Finna record ID"), max_length=1024, null=True, blank=True
    )
    crop_x = models.FloatField(
        verbose_name=_("Crop x coordinate from left"), null=True, blank=True
    )
    crop_y = models.FloatField(
        verbose_name=_("Crop y coordinate from top"), null=True, blank=True
    )
    crop_width = models.FloatField(verbose_name=_("Crop width"), null=True, blank=True)
    crop_height = models.FloatField(
        verbose_name=_("Crop height"), null=True, blank=True
    )
    original_width = models.FloatField(
        verbose_name=_("Original image width"), null=True, blank=True
    )
    original_height = models.FloatField(
        verbose_name=_("Original image height"), null=True, blank=True
    )
    fullimg_original_width = models.FloatField(
        verbose_name=_("Full res original image width"), null=True, blank=True
    )
    fullimg_original_height = models.FloatField(
        verbose_name=_("Full res original image height"), null=True, blank=True
    )

    # Order must always specify a URL where the printing service can download the desired image
    # This can be either as direct URL to HKM image server holding the original image OR URL to
    # kuvaselaamo server to the cropped image
    image_url = models.CharField(
        verbose_name=_("Image URL"), max_length=2048, null=True, blank=True
    )
    crop_image_url = models.CharField(
        verbose_name=_("Cropped Image URL"), max_length=2048, null=True, blank=True
    )
    # If this order is made from Record in collection, the Record is saved for
    # statistics purposes
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        verbose_name=_("Record"),
        null=True,
        blank=True,
    )

    form_phase = models.IntegerField(verbose_name=_("Order form phase"), default=1)
    order_hash = models.CharField(
        verbose_name=_("Randomized order identifier phrase"),
        max_length=1024,
        null=True,
        blank=True,
        unique=True,
    )
    product_type = models.ForeignKey(
        PrintProduct,
        on_delete=models.CASCADE,
        verbose_name=_("Product type"),
        null=True,
        blank=True,
    )
    product_name = models.CharField(
        verbose_name=_("Product Name"), max_length=1024, null=True, blank=True
    )
    # Price and amount information as they were at the time order was made
    # NOTE: Product prizing might vary so these need to be freezed here
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("Amount"), default=1
    )
    postal_fees = models.DecimalField(
        verbose_name=_("Shipping fees"),
        decimal_places=2,
        max_digits=10,
        null=False,
        blank=False,
        default=settings.HKM_POSTAL_FEES,
    )
    unit_price = models.DecimalField(
        verbose_name=_("Unit price"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        verbose_name=_("Total price"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
    )
    total_price_with_postage = models.DecimalField(
        verbose_name=_("Total price with postage"),
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
    )

    # Timestamp for when users has confimed the order in kuvaselaamo
    datetime_confirmed = models.DateTimeField(
        verbose_name=_("Confirmed"), null=True, blank=True
    )

    # Timestamps and state information about payment and checkout
    datetime_checkout_started = models.DateTimeField(
        verbose_name=_("Checkout started"), null=True, blank=True
    )
    datetime_checkout_ended = models.DateTimeField(
        verbose_name=_("Checkout ended"), null=True, blank=True
    )
    is_checkout_successful = models.NullBooleanField(
        verbose_name=_("Checkout successful"), null=True, blank=True
    )

    # Timestamps and state information about payment actually being processed
    datetime_payment_processed = models.DateTimeField(
        verbose_name=_("Payment processed at"), null=True, blank=True
    )
    is_payment_successful = models.NullBooleanField(
        verbose_name=_("Payment successful"), null=True, blank=True
    )

    # Timestamps and state information about the actual product order from
    # print
    datetime_order_started = models.DateTimeField(
        verbose_name=_("Order started"), null=True, blank=True
    )
    datetime_order_ended = models.DateTimeField(
        verbose_name=_("Order ended"), null=True, blank=True
    )
    is_order_successful = models.NullBooleanField(
        verbose_name=_("Order successful"), null=True, blank=True
    )

    # A product order may belong to a collection of orders (multiple prints ordered at once)
    order = models.ForeignKey(
        "ProductOrderCollection",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_orders",
    )

    objects = ProductOrderQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.order_hash:
            self.order_hash = get_random_string(20)
        return super().save(*args, **kwargs)

    @classmethod
    def delete_old_data(cls, date):
        return cls.objects.filter(user__isnull=True, modified__lte=date).delete()

    def __str__(self):
        return self.order_hash


class Feedback(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("User"), null=True, blank=True
    )
    record_id = models.CharField(
        verbose_name=_("Finna record ID"), max_length=1024, null=True, blank=True
    )
    full_name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True
    )
    email = models.EmailField(
        max_length=255, verbose_name=_("Email"), null=True, blank=True
    )
    content = models.TextField(verbose_name=_("Content"))
    is_notification_sent = models.BooleanField(
        verbose_name=_("Notification sent"), default=False
    )
    sent_from = models.CharField(
        verbose_name=_("Sent from"), max_length=500, null=True, blank=True
    )

    @classmethod
    def delete_old_data(cls, date):
        return cls.objects.filter(user__isnull=True, modified__lte=date).delete()


def get_tmp_upload_path(instance, filename):
    return f"tmp/{filename}"


class TmpImage(BaseModel):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Creator"), blank=True, null=True
    )
    record_id = models.CharField(verbose_name=_("Finna record ID"), max_length=1024)
    record_title = models.CharField(verbose_name=_("Title"), max_length=1024)
    edited_image = models.ImageField(
        verbose_name=_("Edited image"), upload_to=get_tmp_upload_path
    )

    @classmethod
    def delete_old_data(cls, date):
        return cls.objects.filter(modified__lte=date, creator__isnull=True).delete()

    def __str__(self):
        return self.record_title


class PageContent(BaseModel, TranslatableModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    identifier = models.CharField(
        verbose_name=_("Identifier"), max_length=255, unique=True
    )
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        content=models.TextField(verbose_name=_("Content")),
    )

    def __str__(self):
        return self.name


class ProductOrderDiscount(models.Model):
    # A log of used discounts
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    order = models.ForeignKey("ProductOrderCollection", on_delete=models.CASCADE)
    code_used = models.CharField(
        max_length=255, verbose_name=_("Used discount code"), null=True
    )
    discounted_value = models.DecimalField(max_digits=6, decimal_places=2)


class ProductOrderCollection(models.Model):
    # A bundle of ProductOrder's for in museum purchases.
    orderer_name = models.CharField(verbose_name=_("Orderer's name"), max_length=255)
    total_price = models.DecimalField(
        verbose_name=_("Total order price"), max_digits=6, decimal_places=2
    )
    sent_to_print = models.BooleanField(
        default=False, verbose_name=_("Sent to printer")
    )

    is_checkout_successful = models.NullBooleanField(
        verbose_name=_("Checkout successful"), null=True, blank=True
    )
    is_payment_successful = models.NullBooleanField(
        verbose_name=_("Payment successful"), null=True, blank=True
    )

    is_order_successful = models.NullBooleanField(
        verbose_name=_("Order successful"), null=True, blank=True
    )

    order_hash = models.CharField(
        verbose_name=_("Randomized order collection identifier phrase"),
        max_length=1024,
        null=True,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return f"{self.orderer_name} - order"

    def save(self, *args, **kwargs):
        if not self.order_hash:
            self.order_hash = get_random_string(20)
        return super().save(*args, **kwargs)

    @property
    def customer_email(self):
        return self.product_orders.first().email
