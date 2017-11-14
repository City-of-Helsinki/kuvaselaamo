# -*- coding: utf-8 -*-
from django.conf import settings
from django.http.response import Http404


def restrict_for_museum(func):
    def view(request, *args, **kwargs):

        if request.user.is_authenticated() and request.user.groups.filter(name=settings.MUSEUM_GROUP).exists():
            raise Http404()

        return func(request, *args, **kwargs)
    return view
