
# -*- coding: utf-8 -*-

import logging
from celery import task
from django.core.mail import send_mail
from hkm.models import Feedback

LOG = logging.getLogger(__name__)


@task(ignore_result=True)
def send_feedback_notification(feedback_id, force=False):
  try:
    feedback = Feedback.objects.get(id=feedback_id)
  except Feedback.DoesNotExist:
    LOG.error('Feedback does not exists', extra={'data': {'feedback_id': feedback_id}})
    return False
  else:
    if not feedback.is_notification_sent or force:
      #title = 'Kuvaselaamopalaute'
      #if feedback.record_id:
      #  title = title + ' %s' % feedback.record_id
      #send_mail(
      #  title,
      #  feedback.content,
      #)
      return True
    else:
      LOG.debug('Notification about feedback is already sent. Not sending again. User "force" flag to re-send notification',
          extra={'data': {'feedback_id': feedback_id}})
    return False


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
