import pytest
from factories import FeedbackFactory, TmpImageFactory, ProductOrderFactory, UserFactory
from hkm.models.models import Feedback, TmpImage, ProductOrder, UserProfile, User, Collection, Record
from django.core.management import call_command
from freezegun import freeze_time
from datetime import datetime, timedelta
from hkm.management.commands.clean_unused_data import DEFAULT_DAYS_UNTIL_REMOVAL, DEFAULT_DAYS_UNTIL_NOTIFICATION

CUSTOM_DAYS_UNTIL_REMOVAL = 10
CUSTOM_DAYS_UNTIL_NOTIFICATION = 5


@pytest.fixture
def day_older_than_removal_date():
    return datetime.today() - timedelta(days=DEFAULT_DAYS_UNTIL_REMOVAL + 1)


@pytest.fixture
def day_newer_than_removal_date():
    return datetime.today() - timedelta(days=DEFAULT_DAYS_UNTIL_REMOVAL - 1)


@pytest.fixture
def day_within_grace_period():
    return datetime.today() - timedelta(days=DEFAULT_DAYS_UNTIL_REMOVAL - DEFAULT_DAYS_UNTIL_NOTIFICATION - 1)


@pytest.fixture
def day_outside_grace_period():
    return datetime.today() - timedelta(days=DEFAULT_DAYS_UNTIL_REMOVAL - DEFAULT_DAYS_UNTIL_NOTIFICATION + 1)


@pytest.fixture
def day_older_than_custom_removal_date():
    return datetime.today() - timedelta(days=CUSTOM_DAYS_UNTIL_REMOVAL + 1)


@pytest.fixture
def day_newer_than_custom_removal_date():
    return datetime.today() - timedelta(days=CUSTOM_DAYS_UNTIL_REMOVAL - 1)


@pytest.fixture
def day_within_custom_grace_period():
    return datetime.today() - timedelta(days=CUSTOM_DAYS_UNTIL_REMOVAL - CUSTOM_DAYS_UNTIL_NOTIFICATION - 1)


@pytest.fixture
def day_outside_custom_grace_period():
    return datetime.today() - timedelta(days=CUSTOM_DAYS_UNTIL_REMOVAL - CUSTOM_DAYS_UNTIL_NOTIFICATION + 1)


@pytest.mark.django_db
def test_that_old_anonymous_data_is_removed_using_default_date(day_older_than_removal_date,
                                                               day_newer_than_removal_date):
    _create_anonymous_data(day_older_than_removal_date)
    _create_anonymous_data(day_newer_than_removal_date)

    _assert_anonymous_data_counts(2)

    call_command('clean_unused_data')

    _assert_anonymous_data_counts(1)


def _create_anonymous_data(modified_date):
    with freeze_time(modified_date):
        FeedbackFactory()
        TmpImageFactory()
        ProductOrderFactory()


@pytest.mark.django_db
def test_that_old_anonymous_data_is_removed_using_custom_date(day_older_than_custom_removal_date,
                                                              day_newer_than_custom_removal_date):
    _create_anonymous_data(day_older_than_custom_removal_date)
    _create_anonymous_data(day_newer_than_custom_removal_date)

    _assert_anonymous_data_counts(2)

    call_command('clean_unused_data', days_until_removal=CUSTOM_DAYS_UNTIL_REMOVAL,
                 days_until_notification=CUSTOM_DAYS_UNTIL_NOTIFICATION)

    _assert_anonymous_data_counts(1)


def _assert_anonymous_data_counts(count):
    assert Feedback.objects.count() == count
    assert TmpImage.objects.count() == count
    assert ProductOrder.objects.count() == count


@pytest.mark.django_db
def test_that_old_user_gets_deleted_using_default_date(day_older_than_removal_date, day_newer_than_removal_date,
                                                       day_outside_grace_period, day_within_grace_period):
    not_deleted = [
        UserFactory(last_login=day_newer_than_removal_date, profile__removal_notification_sent=None),
        UserFactory(last_login=day_newer_than_removal_date, profile__removal_notification_sent=day_within_grace_period)
    ]

    UserFactory(last_login=day_older_than_removal_date, profile__removal_notification_sent=day_outside_grace_period)

    _assert_user_data_counts(3)

    call_command('clean_unused_data')

    _assert_user_data_counts(2)
    _assert_users_exist(not_deleted)


@pytest.mark.django_db
def test_that_old_user_gets_deleted_using_custom_date(day_older_than_custom_removal_date,
                                                      day_newer_than_custom_removal_date,
                                                      day_outside_custom_grace_period):
    not_deleted = [UserFactory(last_login=day_newer_than_custom_removal_date)]

    UserFactory(last_login=day_older_than_custom_removal_date,
                profile__removal_notification_sent=day_outside_custom_grace_period)

    _assert_user_data_counts(2)

    call_command('clean_unused_data', days_until_removal=CUSTOM_DAYS_UNTIL_REMOVAL,
                 days_until_notification=CUSTOM_DAYS_UNTIL_NOTIFICATION)

    _assert_user_data_counts(1)
    _assert_users_exist(not_deleted)


def _assert_user_data_counts(count):
    assert User.objects.count() == count
    assert UserProfile.objects.count() == count
    assert Feedback.objects.count() == count
    assert TmpImage.objects.count() == count
    assert ProductOrder.objects.count() == count
    assert Collection.objects.count() == count
    assert Record.objects.count() == count


@pytest.mark.django_db
def test_that_staff_users_dont_get_deleted(day_older_than_removal_date):
    not_deleted = [
        UserFactory(last_login=day_older_than_removal_date, is_superuser=True),
        UserFactory(last_login=day_older_than_removal_date, is_staff=True),
        UserFactory(last_login=day_older_than_removal_date, profile__is_museum=True),
        UserFactory(last_login=day_older_than_removal_date, profile__is_admin=True)
    ]

    _assert_user_data_counts(4)

    call_command('clean_unused_data')

    _assert_user_data_counts(4)
    _assert_users_exist(not_deleted)


def _assert_users_exist(users):
    for user in users:
        assert User.objects.get(pk=user.id)


@pytest.mark.django_db
def test_that_user_is_not_deleted_without_notification(day_older_than_removal_date, day_within_grace_period,
                                                       day_outside_grace_period):
    not_deleted = [
        UserFactory(last_login=day_older_than_removal_date, profile__removal_notification_sent=None),
        UserFactory(last_login=day_older_than_removal_date, profile__removal_notification_sent=day_within_grace_period)
    ]

    UserFactory(last_login=day_older_than_removal_date, profile__removal_notification_sent=day_outside_grace_period)

    _assert_user_data_counts(3)

    call_command('clean_unused_data')

    _assert_user_data_counts(2)
    _assert_users_exist(not_deleted)


@pytest.mark.django_db
def test_that_user_is_not_deleted_without_notification_using_custom_dates(
        day_older_than_custom_removal_date, day_within_custom_grace_period,
        day_outside_custom_grace_period):
    not_deleted = [
        UserFactory(last_login=day_older_than_custom_removal_date, profile__removal_notification_sent=None),
        UserFactory(last_login=day_older_than_custom_removal_date,
                    profile__removal_notification_sent=day_within_custom_grace_period)
    ]

    UserFactory(last_login=day_older_than_custom_removal_date,
                profile__removal_notification_sent=day_outside_custom_grace_period)

    _assert_user_data_counts(3)

    call_command('clean_unused_data', days_until_removal=CUSTOM_DAYS_UNTIL_REMOVAL,
                 days_until_notification=CUSTOM_DAYS_UNTIL_NOTIFICATION)

    _assert_user_data_counts(2)
    _assert_users_exist(not_deleted)


def test_negative_days_until_removal(capsys):
    call_command('clean_unused_data', days_until_removal=-1)

    assert "Invalid parameters given." in capsys.readouterr()[0]


def test_negative_days_until_notification(capsys):
    call_command('clean_unused_data', days_until_notification=-1)

    assert "Invalid parameters given." in capsys.readouterr()[0]


def test_days_until_notification_cant_be_more_than_days_until_removal(capsys):
    call_command('clean_unused_data', days_until_notification=10, days_until_removal=9)

    assert "Invalid parameters given." in capsys.readouterr()[0]
