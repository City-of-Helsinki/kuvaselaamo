
# -*- coding: utf-8 -*-

from django.conf.urls import url
from hkm import views

urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='hkm_index'),
  url(r'^info/$', views.InfoView.as_view(), name='hkm_info'),
  url(r'^collections/public/$', views.PublicCollectionsView.as_view(), name='hkm_public_collections'),
  url(r'^collections/my/$', views.MyCollectionsView.as_view(), name='hkm_my_collections'),
  url(r'^collections/(?P<collection_id>\d+)/$', views.CollectionDetailView.as_view(), name='hkm_collection'),
  url(r'^collection/(?P<collection_id>\d+)/image/(?P<image_id>\d+)/$', views.ImageDetailView.as_view(), name='hkm_collection_image'),
  url(r'^image/(?P<image_id>\d+)/feedback/$', views.ImageFeedbackView.as_view(), name='hkm_image_feedback'),
  url(r'^image/(?P<finna_id>\d+)/edit/add/$', views.ImageEditAddToCollectionView.as_view(), name='hkm_image_edit_add'),
  url(r'^image/(?P<finna_id>\d+)/edit/download/$', views.ImageEditDownloadView.as_view(), name='hkm_image_edit_download'),
  url(r'^image/(?P<finna_id>\d+)/edit/order/$', views.ImageEditOrderView.as_view(), name='hkm_image_edit_order'),
  url(r'^search/$', views.SearchView.as_view(), name='hkm_search'),
  url(r'^signup/$', views.SignUpView.as_view(), name='hkm_signup'),
]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
