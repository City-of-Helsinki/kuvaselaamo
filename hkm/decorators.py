from django.http.response import Http404


def restrict_for_museum(func):
    def view(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.profile.is_museum:
            raise Http404()

        return func(request, *args, **kwargs)

    return view
