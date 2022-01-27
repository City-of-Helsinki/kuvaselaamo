from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from hkm.models.models import Feedback, ProductOrder, TmpImage

DEFAULT_DAYS_UNTIL_REMOVAL = 365
DEFAULT_DAYS_UNTIL_NOTIFICATION = 335


class Command(BaseCommand):
    help = "Clean unused data from application."

    def add_arguments(self, parser):
        parser.add_argument(
            "-dr",
            "--days_until_removal",
            type=int,
            help="Specifies the time in days for which old data is deleted.",
            default=DEFAULT_DAYS_UNTIL_REMOVAL,
        )
        parser.add_argument(
            "-dn",
            "--days_until_notification",
            type=int,
            help="Specifies the time in days after which a notification warning about removal will be sent to users.",
            default=DEFAULT_DAYS_UNTIL_NOTIFICATION,
        )

    def handle(self, *args, **kwargs):
        days_until_removal = kwargs["days_until_removal"]
        days_until_notification = kwargs["days_until_notification"]

        if (
            days_until_removal < 0
            or days_until_notification < 0
            or days_until_removal < days_until_notification
        ):
            self.stdout.write(
                self.style.ERROR(
                    "Invalid parameters given. Ensure that days_until_removal and days_until_notification are positive "
                    "integers and that days_until_removal > days_until_notification"
                )
            )
            return

        grace_period_length_days = days_until_removal - days_until_notification
        self.stdout.write(
            f"Old data cleaning started! Removing data older than {days_until_removal} "
            f"days. Waiting for {grace_period_length_days} days after "
            f"notification has been sent before removing old User data."
        )

        counted_date = timezone.now() - timedelta(days=days_until_removal)
        grace_period_start = timezone.now() - timedelta(days=grace_period_length_days)

        # Find and delete unused users. Do not delete superusers or staff users.
        users = User.objects.filter(
            last_login__lte=counted_date,
            is_superuser=False,
            is_staff=False,
            profile__is_museum=False,
            profile__is_admin=False,
            profile__removal_notification_sent__lte=grace_period_start,
        ).delete()

        # Find and delete old TmpImages, Feedbacks and Orders
        temps = TmpImage.delete_old_data(counted_date)
        feedbacks = Feedback.delete_old_data(counted_date)
        orders = ProductOrder.delete_old_data(counted_date)

        self.stdout.write(
            self.style.SUCCESS(
                f"Old data cleaning finished! Removed {users[0]} user-related "
                f"object(s), {temps[0]} temp(s), {feedbacks[0]} feedback(s), "
                f"{orders[0]} order(s)"
            )
        )
