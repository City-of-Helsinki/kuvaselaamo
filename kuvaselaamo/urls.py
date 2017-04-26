# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


class AdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_superuser


admin.site = AdminSite()
admin.autodiscover()

handler404 = 'hkm.views.handler404'
handler500 = 'hkm.views.handler500'

admin_urls = [
    url(r'^sysadmin/', include(admin.site.urls)),
]

app_urls = [
    url(r'^', include('hkm.urls')),
]

auth_urls = [
    url(r'^', include('django.contrib.auth.urls')),
]

static_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_urls += staticfiles_urlpatterns()

urlpatterns = admin_urls + app_urls + static_urls + auth_urls

if settings.DEBUG:
    from django.views.generic import TemplateView

    class ServerError(TemplateView):
        template_name = '500.html'

    class PageNotFoundError(TemplateView):
        template_name = '404.html'

    urlpatterns += [
        url(r'^500/$', ServerError.as_view()),
        url(r'^404/$', PageNotFoundError.as_view()),
    ]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
