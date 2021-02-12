from django.conf import settings


def global_settings(request):
    return {
        'ENABLE_ANALYTICS': settings.ENABLE_ANALYTICS
    }
