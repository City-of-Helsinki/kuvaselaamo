
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from hkm import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='hkm_index'),
    url(r'^info/$', views.InfoView.as_view(), name='hkm_info'),

    url(r'^about/$', views.SiteinfoAboutView.as_view(), name='hkm_siteinfo_about'),
    url(r'^privacy/$', views.SiteinfoPrivacyView.as_view(),
        name='hkm_siteinfo_privacy'),
    url(r'^QA/$', views.SiteinfoQAView.as_view(), name='hkm_siteinfo_QA'),
    url(r'^terms/$', views.SiteinfoTermsView.as_view(), name='hkm_siteinfo_terms'),

    url(r'^collection/public/$', views.PublicCollectionsView.as_view(),
        name='hkm_public_collections'),
    url(r'^collection/my/$', login_required()
        (views.MyCollectionsView.as_view()), name='hkm_my_collections'),
    url(r'^collection/(?P<collection_id>\d+)/$',
        views.CollectionDetailView.as_view(), name='hkm_collection'),

    url(r'^record/(?P<finna_id>[a-zA-Z0-9:.]+)/$',
        views.FinnaRecordDetailView.as_view(), name='hkm_record'),
    url(r'^record/(?P<finna_id>[a-zA-Z0-9:.]+)/feedback/$',
        views.FinnaRecordFeedbackView.as_view(), name='hkm_record_feedback'),

    url(r'^search/$', views.SearchView.as_view(), name='hkm_search'),
    url(r'^search/record/$', views.SearchRecordDetailView.as_view(),
        name='hkm_search_record'),

    url(r'^signup/$', views.SignUpView.as_view(), name='hkm_signup'),
    url(r'^language/$', views.LanguageView.as_view(), name='hkm_language'),

    url(r'^order/(?P<finna_id>[a-zA-Z0-9:.]+)/$',
        views.CreateOrderView.as_view(), name='hkm_order_create'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/product/$',
        views.OrderProductView.as_view(), name='hkm_order_product'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/contact/$',
        views.OrderContactInformationView.as_view(), name='hkm_order_contact_information'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/summary/$',
        views.OrderSummaryView.as_view(), name='hkm_order_summary'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/confirmation/$',
        views.OrderConfirmation.as_view(), name='hkm_order_confirmation'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/show_result/$',
        views.OrderShowResultView.as_view(), name='hkm_order_show_result'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/notify/$',
        views.OrderPBWNotify.as_view(), name='hkm_order_pbw_notify'),

    url(r'^ajax/record/fav/$', login_required()(views.AjaxUserFavoriteRecordView.as_view()),
        name='hkm_ajax_record_fav'),
    url(r'^ajax/crop/$', views.AjaxCropRecordView.as_view(),
        name='hkm_ajax_crop'),


]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
