# -*- coding: utf-8 -*-
from django import forms
from hkm.forms import ShowcaseForm
from django.core.exceptions import ValidationError
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.template import loader, RequestContext
from django.urls import reverse
from django.utils.html import format_html
from parler.admin import TranslatableAdmin

from hkm.models import models
from hkm.models.campaigns import Campaign, CampaignCode


class CampaignAdmin(TranslatableAdmin):

    readonly_fields = ["campaign_code_actions"]

    def get_urls(self):
        urls = super(CampaignAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<campaign_id>.+)/generate/$',
                self.admin_site.admin_view(self.generate),
                name='generate-campaign-codes',
            )
        ]
        return custom_urls + urls

    def generate(self, request, campaign_id, *args, **kwargs):
        campaign = Campaign.objects.get(pk=campaign_id)
        for i in range(0, int(request.POST.get("amount", 0))):
            code = CampaignCode(campaign=campaign)
            code.generate_code(
                length=int(request.POST.get("length")),
                prefix=request.POST.get("prefix"),
            )
            code.save()
        return JsonResponse({"success": "ok"})

    def campaign_code_actions(self, obj):
        html = loader.render_to_string("hkm/snippets/generate_codes.html", context={"obj": obj})
        return html

    campaign_code_actions.short_description = 'Alennuskoodien generointi'

    class Media:
        js = ('hkm/js/campaign_admin.js',)


class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'campaign')
    list_filter = ('status', 'campaign', 'campaign__usable_from', 'campaign__usable_to')


class PageContentAdmin(TranslatableAdmin):

    class Media:
        js = ('ckeditor/ckeditor.js', 'hkm/js/init.js')


class ShowcaseAdmin(admin.ModelAdmin):
    form = ShowcaseForm
    filter_horizontal = ['albums']


admin.site.register(models.UserProfile)
admin.site.register(models.Collection)
admin.site.register(models.Record)
admin.site.register(models.Showcase, ShowcaseAdmin)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(models.PrintProduct)
admin.site.register(models.ProductOrder)
admin.site.register(models.Feedback)
admin.site.register(models.TmpImage)
admin.site.register(models.ProductOrderCollection)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignCode, CodeAdmin)
admin.site.register(models.PageContent, PageContentAdmin)


