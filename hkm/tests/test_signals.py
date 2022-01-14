from datetime import datetime, timedelta

import pytest
from django.contrib.auth import signals
from django.test.client import RequestFactory

from hkm.models.models import UserProfile

from .factories import UserFactory


@pytest.mark.django_db
def test_that_login_clears_removal_notification_timestamp():
    user = UserFactory(
        profile__removal_notification_sent=datetime.today() - timedelta(days=1)
    )

    assert UserProfile.objects.first().removal_notification_sent

    request = RequestFactory().get("/login")
    signals.user_logged_in.send(sender=user.__class__, request=request, user=user)

    assert not UserProfile.objects.first().removal_notification_sent
