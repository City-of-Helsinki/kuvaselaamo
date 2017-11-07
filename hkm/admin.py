# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User, Group
from parler.admin import TranslatableAdmin

from hkm.models import models
from hkm.models.campaigns import Campaign, CampaignCode


class CampaignAdmin(TranslatableAdmin):

    def campaign_code_actions(self, obj):
        pass
        # TODO: Render action buttons


class CodeAdmin(admin.ModelAdmin):
    list_display = ("code", "campaign")
    list_filter = ("status", "campaign", "campaign__usable_from", "campaign__usable_to")


class PageContentAdmin(TranslatableAdmin):

    class Media:
        js = ('ckeditor/ckeditor.js', 'hkm/js/init.js')


admin.site.register(models.UserProfile)
admin.site.register(models.Collection)
admin.site.register(models.Record)
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


