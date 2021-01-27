from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hkm.models.models import TmpImage, Feedback, ProductOrder
from datetime import timedelta
from django.utils import timezone

DEFAULT_DAYS = 365

class Command(BaseCommand):
    help = "Clean unused data from application."

    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--days", type=int, help="Specifies the time in days for which old data is deleted", default=DEFAULT_DAYS
        )

    def handle(self, *args, **kwargs):
        days = kwargs['days']
        if not days:
            days = DEFAULT_DAYS

        self.stdout.write("Old data cleaning started! Removing data older than " + str(days) + " days.")
        counted_date = timezone.now() - timedelta(days=days)

        # Find and delete unused users. Do not delete superusers or staff users.
        users = User.objects.filter(last_login__lte=counted_date, is_superuser=False, is_staff=False,
                                    profile__is_museum=False, profile__is_admin=False).delete()
        print(users)

        # Find and delete old TmpImages, Feedbacks and Orders
        temps = TmpImage.delete_old_data(counted_date)
        feedbacks = Feedback.delete_old_data(counted_date)
        orders = ProductOrder.delete_old_data(counted_date)

        self.stdout.write(self.style.SUCCESS('Old data cleaning finished! Removed %s user(s), %s temp(s), '
                                             '%s feedback(s), %s order(s)' % (users[0], temps[0], feedbacks[0], orders[0])))
