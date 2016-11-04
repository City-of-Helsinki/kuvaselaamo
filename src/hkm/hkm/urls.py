
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from hkm import views

urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='hkm_index'),
  url(r'^info/$', views.InfoView.as_view(), name='hkm_info'),

  url(r'^collection/public/$', views.PublicCollectionsView.as_view(), name='hkm_public_collections'),
  url(r'^collection/my/$', login_required()(views.MyCollectionsView.as_view()), name='hkm_my_collections'),
  url(r'^collection/(?P<collection_id>\d+)/$', views.CollectionDetailView.as_view(), name='hkm_collection'),

  url(r'^record/(?P<finna_id>.+)/$', views.FinnaRecordDetailView.as_view(), name='hkm_record'),
  url(r'^record/(?P<finna_id>.+)/feedback/$', views.FinnaRecordFeedbackView.as_view(), name='hkm_record_feedback'),

  url(r'^search/$', views.SearchView.as_view(), name='hkm_search'),
  url(r'^search/record/$', views.SearchRecordDetailView.as_view(), name='hkm_search_record'),

  url(r'^signup/$', views.SignUpView.as_view(), name='hkm_signup'),
  url(r'^language/$', views.LanguageView.as_view(), name='hkm_language'),

  url(r'^ajax/record/fav/$', login_required()(views.AjaxUserFavoriteRecordView.as_view()),
    name='hkm_ajax_record_fav'),

]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
