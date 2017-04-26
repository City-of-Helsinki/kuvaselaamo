def settings(context):
    from django.conf import settings
    return {
        'MY_DOMAIN': settings.HKM_MY_DOMAIN,
    }
