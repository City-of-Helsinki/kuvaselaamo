
# -*- coding: utf-8 -*-

import logging
from celery import task
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.core.mail import send_mail
from hkm.models import Feedback
from hkm import settings

LOG = logging.getLogger(__name__)


@task(ignore_result=True)
def send_feedback_notification(feedback_id, force=False):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
    except Feedback.DoesNotExist:
        LOG.error('Feedback does not exists', extra={
                  'data': {'feedback_id': feedback_id}})
        return False
    else:
        if not feedback.is_notification_sent or force:
            title = _(u'Kuvaselaamopalaute')
            message = render_to_string(
                'hkm/emails/feedback.txt', {'feedback': feedback, 'MY_DOMAIN': settings.MY_DOMAIN})
            count_sent_message = send_mail(
                title,
                message,
                settings.FEEDBACK_FROM_EMAIL,
                settings.FEEDBACK_NOTIFICATION_EMAILS,
                fail_silently=False,
            )
            if count_sent_message == 1:
                feedback.is_notification_sent = True
                feedback.save()
                return True
            else:
                LOG.error('send_mail returned 0 sent messages')
        else:
            LOG.debug('Notification about feedback is already sent. Not sending again. User "force" flag to re-send notification',
                      extra={'data': {'feedback_id': feedback_id}})
        return False


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
