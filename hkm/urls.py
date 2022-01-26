from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from hkm.decorators import restrict_for_museum
from hkm.views import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="hkm_home"),
    path("info/", views.InfoView.as_view(), name="hkm_info"),
    path("about/", views.SiteinfoAboutView.as_view(), name="hkm_siteinfo_about"),
    path(
        "accessibility/",
        views.SiteinfoAccessibilityView.as_view(),
        name="hkm_siteinfo_accessibility",
    ),
    path("privacy/", views.SiteinfoPrivacyView.as_view(), name="hkm_siteinfo_privacy"),
    path("QA/", views.SiteinfoQAView.as_view(), name="hkm_siteinfo_QA"),
    path("terms/", views.SiteinfoTermsView.as_view(), name="hkm_siteinfo_terms"),
    path(
        "collection/public/",
        views.PublicCollectionsView.as_view(),
        name="hkm_public_collections",
    ),
    path(
        "collection/my/",
        restrict_for_museum(login_required()(views.MyCollectionsView.as_view())),
        name="hkm_my_collections",
    ),
    path(
        "collection/<int:collection_id>/",
        views.CollectionDetailView.as_view(),
        name="hkm_collection",
    ),
    path("search/", views.SearchView.as_view(), name="hkm_search"),
    path(
        "search/details/",
        views.SearchRecordDetailView.as_view(),
        name="hkm_search_record",
    ),
    path(
        "record/feedback/",
        views.RecordFeedbackView.as_view(),
        name="hkm_record_feedback",
    ),
    re_path(
        r"^record/(?P<finna_id>[a-zA-Z0-9:.]+)/$",
        views.LegacyRecordDetailView.as_view(),
        name="hkm_legacy_record_details",
    ),
    path("signup/", restrict_for_museum(views.SignUpView.as_view()), name="hkm_signup"),
    path("language/", views.LanguageView.as_view(), name="hkm_language"),
    path(
        "ajax/record/fav/",
        restrict_for_museum(
            login_required()(views.AjaxUserFavoriteRecordView.as_view())
        ),
        name="hkm_ajax_record_fav",
    ),
    path("ajax/crop/", views.AjaxCropRecordView.as_view(), name="hkm_ajax_crop"),
    path(
        "ajax/collection/",
        views.AjaxAddToCollection.as_view(),
        name="hkm_add_to_collection",
    ),
    path("reset/", views.PasswordResetConfirmViewNew.as_view(), name="reset_pwd"),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmViewNew.as_view(),
        name="reset_pwd",
    ),
]
