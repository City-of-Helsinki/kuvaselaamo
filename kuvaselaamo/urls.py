from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path


class AdminSite(admin.AdminSite):
    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_staff
            and request.user.is_superuser
        )


admin.site = AdminSite()
admin.autodiscover()

handler404 = "hkm.views.views.handler404"
handler500 = "hkm.views.views.handler500"

admin_urls = [
    path("sysadmin/", admin.site.urls),
]

app_urls = [
    path("", include("hkm.urls")),
]

auth_urls = [
    path("", include("django.contrib.auth.urls")),
]

static_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls += staticfiles_urlpatterns()

urlpatterns = admin_urls + app_urls + static_urls + auth_urls

if settings.DEBUG:
    from django.views.generic import TemplateView

    class ServerError(TemplateView):
        template_name = "hkm/views/500.html"

    class PageNotFoundError(TemplateView):
        template_name = "hkm/views/404.html"

    urlpatterns += [
        path("500/", ServerError.as_view()),
        path("404/", PageNotFoundError.as_view()),
    ]


#
# Kubernetes liveness & readiness probes
#
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    return HttpResponse(status=200)


urlpatterns += [path("healthz", healthz), path("readiness", readiness)]
