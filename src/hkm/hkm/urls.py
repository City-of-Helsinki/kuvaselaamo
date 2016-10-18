
# -*- coding: utf-8 -*-

from django.conf.urls import url
from hkm.views import IndexView

urlpatterns = [
  url(r'^$', IndexView.as_view(), name='hkm_index'),
]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
