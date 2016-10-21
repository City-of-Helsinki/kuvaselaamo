
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from hkm import models


admin.site.register(models.UserProfile)
admin.site.register(models.Collection)
admin.site.register(models.Record)
admin.site.register(User)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
