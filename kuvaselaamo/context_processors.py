from django.conf import settings


def global_settings(request):
    return {
        "ENABLE_ANALYTICS": settings.ENABLE_ANALYTICS,
        "ENABLE_FEEDBACK_CONGESTION_MSG": settings.ENABLE_FEEDBACK_CONGESTION_MSG,
    }
