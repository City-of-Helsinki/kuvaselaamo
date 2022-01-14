# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from hkm.decorators import restrict_for_museum
from hkm.views import views

urlpatterns = [
    url(r"^$", views.HomeView.as_view(), name="hkm_home"),
    url(r"^info/$", views.InfoView.as_view(), name="hkm_info"),
    url(r"^about/$", views.SiteinfoAboutView.as_view(), name="hkm_siteinfo_about"),
    url(
        r"^accessibility/$",
        views.SiteinfoAccessibilityView.as_view(),
        name="hkm_siteinfo_accessibility",
    ),
    url(
        r"^privacy/$", views.SiteinfoPrivacyView.as_view(), name="hkm_siteinfo_privacy"
    ),
    url(r"^QA/$", views.SiteinfoQAView.as_view(), name="hkm_siteinfo_QA"),
    url(r"^terms/$", views.SiteinfoTermsView.as_view(), name="hkm_siteinfo_terms"),
    url(
        r"^collection/public/$",
        views.PublicCollectionsView.as_view(),
        name="hkm_public_collections",
    ),
    url(
        r"^collection/my/$",
        restrict_for_museum(login_required()(views.MyCollectionsView.as_view())),
        name="hkm_my_collections",
    ),
    url(
        r"^collection/(?P<collection_id>\d+)/$",
        views.CollectionDetailView.as_view(),
        name="hkm_collection",
    ),
    url(r"^search/$", views.SearchView.as_view(), name="hkm_search"),
    url(
        r"^search/details/$",
        views.SearchRecordDetailView.as_view(),
        name="hkm_search_record",
    ),
    url(
        r"^record/feedback/$",
        views.RecordFeedbackView.as_view(),
        name="hkm_record_feedback",
    ),
    url(
        r"^record/(?P<finna_id>[a-zA-Z0-9:.]+)/$",
        views.LegacyRecordDetailView.as_view(),
        name="hkm_legacy_record_details",
    ),
    url(
        r"^signup/$", restrict_for_museum(views.SignUpView.as_view()), name="hkm_signup"
    ),
    url(r"^language/$", views.LanguageView.as_view(), name="hkm_language"),
    url(
        r"^ajax/record/fav/$",
        restrict_for_museum(
            login_required()(views.AjaxUserFavoriteRecordView.as_view())
        ),
        name="hkm_ajax_record_fav",
    ),
    url(r"^ajax/crop/$", views.AjaxCropRecordView.as_view(), name="hkm_ajax_crop"),
    url(
        r"^ajax/collection/$",
        views.AjaxAddToCollection.as_view(),
        name="hkm_add_to_collection",
    ),
    url(r"^reset/$", views.PasswordResetConfirmViewNew.as_view(), name="reset_pwd"),
    url(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.PasswordResetConfirmViewNew.as_view(),
        name="reset_pwd",
    ),
]
