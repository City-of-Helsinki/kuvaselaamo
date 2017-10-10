# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from hkm import views
from hkm.decorators import restrict_for_museum

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
    url(r'^collection/my/$', restrict_for_museum(login_required()
        (views.MyCollectionsView.as_view())), name='hkm_my_collections'),
    url(r'^collection/(?P<collection_id>\d+)/$',
        views.CollectionDetailView.as_view(), name='hkm_collection'),

    url(r'^record/(?P<finna_id>[a-zA-Z0-9:.]+)/$',
        views.FinnaRecordDetailView.as_view(), name='hkm_record'),
    url(r'^record/(?P<finna_id>[a-zA-Z0-9:.]+)/feedback/$',
        restrict_for_museum(views.FinnaRecordFeedbackView.as_view()), name='hkm_record_feedback'),

    url(r'^search/$', restrict_for_museum(views.SearchView.as_view()), name='hkm_search'),
    url(r'^search/record/$', restrict_for_museum(views.SearchRecordDetailView.as_view()),
        name='hkm_search_record'),

    url(r'^signup/$', restrict_for_museum(views.SignUpView.as_view()), name='hkm_signup'),
    url(r'^language/$', views.LanguageView.as_view(), name='hkm_language'),

    url(r'^order/(?P<finna_id>[a-zA-Z0-9:.]+)/$',
        views.CreateOrderView.as_view(), name='hkm_order_create'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/product/$',
        views.OrderProductView.as_view(), name='hkm_order_product'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/contact/$',
        restrict_for_museum(views.OrderContactInformationView.as_view()), name='hkm_order_contact_information'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/summary/$',
        restrict_for_museum(views.OrderSummaryView.as_view()), name='hkm_order_summary'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/confirmation/$',
        restrict_for_museum(views.OrderConfirmation.as_view()), name='hkm_order_confirmation'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/show_result/$',
        restrict_for_museum(views.OrderShowResultView.as_view()), name='hkm_order_show_result'),
    url(r'^order/(?P<order_id>[a-zA-Z0-9]+)/notify/$',
        restrict_for_museum(views.OrderPBWNotify.as_view()), name='hkm_order_pbw_notify'),
    url(r'^ajax/record/fav/$', restrict_for_museum(login_required()(views.AjaxUserFavoriteRecordView.as_view())),
        name='hkm_ajax_record_fav'),
    url(r'^ajax/crop/$', views.AjaxCropRecordView.as_view(),
        name='hkm_ajax_crop'),
    url(r'^basket/$', views.BasketView.as_view(), name='basket'),
    url(r'^basket/checkout/$', views.BasketView.as_view(), {"phase": "checkout"}, name='checkout'),
]


