from datetime import timedelta
from unittest.mock import DEFAULT, patch

import pytest
from anymail.exceptions import AnymailRequestsAPIError
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time

from hkm.management.commands.clean_unused_data import DEFAULT_DAYS_UNTIL_NOTIFICATION
from hkm.models.models import User

from .factories import UserFactory

CUSTOM_DAYS_UNTIL_NOTIFICATION = 5


@pytest.fixture
def day_older_than_notification_date():
    return timezone.now() - timedelta(days=DEFAULT_DAYS_UNTIL_NOTIFICATION + 1)


@pytest.fixture
def day_newer_than_notification_date():
    return timezone.now() - timedelta(days=DEFAULT_DAYS_UNTIL_NOTIFICATION - 1)


@pytest.fixture
def day_older_than_custom_notification_date():
    return timezone.now() - timedelta(days=CUSTOM_DAYS_UNTIL_NOTIFICATION + 1)


@pytest.fixture
def day_newer_than_custom_notification_date():
    return timezone.now() - timedelta(days=CUSTOM_DAYS_UNTIL_NOTIFICATION - 1)


def _assert_email_sent(mailoutbox, emails):
    assert len(mailoutbox) == len(emails)

    for idx, email in enumerate(emails):
        assert mailoutbox[idx].subject
        assert mailoutbox[idx].body
        assert mailoutbox[idx].from_email == "kissa@kissa.com"
        assert mailoutbox[idx].to == [email]


@pytest.mark.django_db
def test_that_old_user_gets_notified_using_default_date(
    day_older_than_notification_date, day_newer_than_notification_date, mailoutbox
):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u2 = UserFactory(
            last_login=day_newer_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u3 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=day_older_than_notification_date,
        )

        call_command("send_removal_notifications")

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u2.id).profile.removal_notification_sent is None
        assert (
            User.objects.get(pk=u3.id).profile.removal_notification_sent
            == day_older_than_notification_date
        )

        _assert_email_sent(mailoutbox, [u1.email])


@pytest.mark.django_db
def test_that_old_user_gets_notified_using_custom_date(
    day_older_than_custom_notification_date,
    day_newer_than_custom_notification_date,
    mailoutbox,
):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_older_than_custom_notification_date,
            profile__removal_notification_sent=None,
        )
        u2 = UserFactory(
            last_login=day_newer_than_custom_notification_date,
            profile__removal_notification_sent=None,
        )
        u3 = UserFactory(
            last_login=day_older_than_custom_notification_date,
            profile__removal_notification_sent=day_older_than_custom_notification_date,
        )

        call_command(
            "send_removal_notifications",
            days_until_notification=CUSTOM_DAYS_UNTIL_NOTIFICATION,
        )

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u2.id).profile.removal_notification_sent is None
        assert (
            User.objects.get(pk=u3.id).profile.removal_notification_sent
            == day_older_than_custom_notification_date
        )

        _assert_email_sent(mailoutbox, [u1.email])


def test_negative_days_until_notification(capsys):
    call_command("send_removal_notifications", days_until_notification=-1)

    assert "Invalid parameters given." in capsys.readouterr()[0]


@pytest.mark.django_db
def test_that_multiple_users_get_notified(day_older_than_notification_date, mailoutbox):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u2 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u3 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )

        call_command("send_removal_notifications")

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u2.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u3.id).profile.removal_notification_sent == now

        _assert_email_sent(mailoutbox, [u1.email, u2.email, u3.email])


@pytest.mark.django_db
def test_no_notifications(day_newer_than_notification_date, mailoutbox):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_newer_than_notification_date,
            profile__removal_notification_sent=None,
        )

        call_command("send_removal_notifications")

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent is None

        _assert_email_sent(mailoutbox, [])


# This test works but only if run as a single test. There's some funny business going on with @patch,
# so this is skipped. Maybe in the future when we get a more current Python version, @patch will start
# working as expected.
@pytest.mark.skip
@pytest.mark.django_db
@patch("django.core.mail.send_mail", side_effect=[DEFAULT, Exception("ka-boom")])
def test_error_during_email_sending(send_mail, day_older_than_notification_date):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u2 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u3 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )

        assert User.objects.count() == 3

        with pytest.raises(Exception):
            call_command("send_removal_notifications")

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u2.id).profile.removal_notification_sent is None
        assert User.objects.get(pk=u3.id).profile.removal_notification_sent is None


@pytest.mark.django_db
@patch(
    "django.core.mail.send_mail",
    side_effect=[DEFAULT, AnymailRequestsAPIError("ka-boom", status_code=400), DEFAULT],
)
def test_invalid_email_error_during_email_sending(
    send_mail, day_older_than_notification_date
):
    now = timezone.now()
    with freeze_time(now):
        u1 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u2 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )
        u3 = UserFactory(
            last_login=day_older_than_notification_date,
            profile__removal_notification_sent=None,
        )

        assert User.objects.count() == 3

        call_command("send_removal_notifications")

        assert User.objects.get(pk=u1.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u2.id).profile.removal_notification_sent == now
        assert User.objects.get(pk=u3.id).profile.removal_notification_sent == now
