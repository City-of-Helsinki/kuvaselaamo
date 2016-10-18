
# -*- coding: utf-8 -*-

from django.contrib import admin
from hkm import models


admin.site.register(models.UserProfile)
admin.site.register(models.Collection)
admin.site.register(models.Image)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
