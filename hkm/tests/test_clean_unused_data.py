import pytest
from factories import FeedbackFactory, TmpImageFactory, ProductOrderFactory, UserFactory
from hkm.models.models import Feedback, TmpImage, ProductOrder, UserProfile, User, Collection, Record
from django.core.management import call_command
from freezegun import freeze_time


@pytest.mark.django_db
def test_that_old_anonymous_data_is_removed(day_older_than_removal_date, day_newer_than_removal_date):
    with freeze_time(day_older_than_removal_date):
        FeedbackFactory()
        TmpImageFactory()
        ProductOrderFactory()

    with freeze_time(day_newer_than_removal_date):
        FeedbackFactory()
        TmpImageFactory()
        ProductOrderFactory()

    assert Feedback.objects.count() == 2
    assert TmpImage.objects.count() == 2
    assert ProductOrder.objects.count() == 2

    call_command('clean_unused_data')

    assert Feedback.objects.count() == 1
    assert TmpImage.objects.count() == 1
    assert ProductOrder.objects.count() == 1


@pytest.mark.django_db
def test_that_old_user_gets_deleted(day_older_than_removal_date, day_newer_than_removal_date):
    UserFactory(last_login=day_older_than_removal_date)

    UserFactory(last_login=day_newer_than_removal_date)

    assert User.objects.count() == 2
    assert UserProfile.objects.count() == 2
    assert Feedback.objects.count() == 2
    assert TmpImage.objects.count() == 2
    assert ProductOrder.objects.count() == 2
    assert Collection.objects.count() == 2
    assert Record.objects.count() == 2

    call_command('clean_unused_data')

    assert User.objects.count() == 1
    assert UserProfile.objects.count() == 1
    assert Feedback.objects.count() == 1
    assert TmpImage.objects.count() == 1
    assert ProductOrder.objects.count() == 1
    assert Collection.objects.count() == 1
    assert Record.objects.count() == 1


@pytest.mark.django_db
def test_that_staff_users_dont_get_deleted(day_older_than_removal_date):
    UserFactory(last_login=day_older_than_removal_date, is_superuser=True)
    UserFactory(last_login=day_older_than_removal_date, is_staff=True)

    assert User.objects.count() == 2

    call_command('clean_unused_data')

    assert User.objects.count() == 2
