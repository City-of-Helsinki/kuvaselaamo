from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.template import loader
from django.urls import re_path
from parler.admin import TranslatableAdmin

from hkm.forms import ShowcaseForm
from hkm.models import models
from hkm.models.campaigns import Campaign, CampaignCode


class CampaignAdmin(TranslatableAdmin):

    readonly_fields = ["campaign_code_actions"]
    list_display = (
        "identifier",
        "name",
        "status",
        "usage_type",
        "user_group",
        "usable_from",
        "usable_to",
        "created_on",
        "modified_on",
    )
    list_filter = (
        "status",
        "usage_type",
        "user_group",
        "usable_from",
        "usable_to",
        "created_on",
        "modified_on",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^(?P<campaign_id>.+)/generate/$",
                self.admin_site.admin_view(self.generate),
                name="generate-campaign-codes",
            )
        ]
        return custom_urls + urls

    def generate(self, request, campaign_id, *args, **kwargs):
        campaign = Campaign.objects.get(pk=campaign_id)
        for _i in range(0, int(request.POST.get("amount", 0))):
            code = CampaignCode(campaign=campaign)
            code.generate_code(
                length=int(request.POST.get("length")),
                prefix=request.POST.get("prefix"),
            )
            code.save()
        return JsonResponse({"success": "ok"})

    def campaign_code_actions(self, obj):
        html = loader.render_to_string(
            "hkm/snippets/generate_codes.html", context={"obj": obj}
        )
        return html

    campaign_code_actions.short_description = "Alennuskoodien generointi"

    class Media:
        js = ("hkm/js/campaign_admin.js",)


class CodeAdmin(admin.ModelAdmin):
    list_display = ("code", "campaign")
    list_filter = ("status", "campaign", "campaign__usable_from", "campaign__usable_to")


class PageContentAdmin(TranslatableAdmin):
    class Media:
        js = ("ckeditor/ckeditor.js", "hkm/js/init.js")

    list_display = (
        "identifier",
        "name",
    )


class ShowcaseAdmin(admin.ModelAdmin):
    form = ShowcaseForm
    filter_horizontal = ["albums"]
    list_display = (
        "id",
        "title",
    )
    search_fields = ("title",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "is_admin", "is_museum", "created", "modified")
    list_filter = ("is_admin", "is_museum", "created", "modified")
    date_hierarchy = "created"
    search_fields = ("user__username",)
    autocomplete_fields = ("user",)


class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "is_public",
        "is_featured",
        "is_showcaseable",
        "collection_type",
    )
    list_filter = ("is_public", "is_featured", "is_showcaseable", "collection_type")
    search_fields = (
        "title",
        "owner__username",
    )
    autocomplete_fields = ("owner",)


class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "record_id",
    )
    search_fields = ("creator__username", "record_id")
    autocomplete_fields = ("creator",)


class PrintProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "width",
        "height",
        "paper_quality",
        "is_museum_only",
    )
    list_filter = ("paper_quality", "is_museum_only")
    search_fields = ("name",)


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_hash",
        "product_name",
        "record",
        "record_finna_id",
        "first_name",
        "last_name",
        "email",
        "datetime_confirmed",
        "is_order_successful",
    )
    list_filter = ("is_order_successful", "datetime_confirmed")
    date_hierarchy = "datetime_confirmed"
    search_fields = (
        "order_hash",
        "record_finna_id",
        "first_name",
        "last_name",
        "email",
    )


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "record_id", "email", "is_notification_sent")
    list_filter = ("is_notification_sent",)


class TmpImageAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "record_id", "record_title")
    search_fields = ("record_title", "record_id")


class ProductOrderCollectionAdmin(admin.ModelAdmin):
    list_display = (
        "order_hash",
        "orderer_name",
        "total_price",
        "sent_to_print",
        "is_checkout_successful",
        "is_payment_successful",
        "is_order_successful",
    )
    list_filter = (
        "sent_to_print",
        "is_checkout_successful",
        "is_payment_successful",
        "is_order_successful",
    )
    search_fields = ("order_hash", "orderer_name")


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Record, RecordAdmin)
admin.site.register(models.Showcase, ShowcaseAdmin)
admin.site.register(User, DjangoUserAdmin)
admin.site.register(Group, DjangoGroupAdmin)
admin.site.register(models.PrintProduct, PrintProductAdmin)
admin.site.register(models.ProductOrder, ProductOrderAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)
admin.site.register(models.TmpImage, TmpImageAdmin)
admin.site.register(models.ProductOrderCollection, ProductOrderCollectionAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignCode, CodeAdmin)
admin.site.register(models.PageContent, PageContentAdmin)
