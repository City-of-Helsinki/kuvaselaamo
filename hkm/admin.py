# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from parler.admin import TranslatableAdmin

from hkm import models


admin.site.register(models.UserProfile)
admin.site.register(models.Collection)
admin.site.register(models.Record)
admin.site.register(User)
admin.site.register(models.PrintProduct)
admin.site.register(models.ProductOrder)
admin.site.register(models.Feedback)
admin.site.register(models.TmpImage)
admin.site.register(models.PageContent, TranslatableAdmin)


