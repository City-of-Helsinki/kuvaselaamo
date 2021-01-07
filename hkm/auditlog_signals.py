import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    logger.info('user logged in: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    logger.debug('user logged out: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning('user login failed: {credentials}'.format(
        credentials=credentials,
    ))
