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

        # Find and delete unused users
        unused_users = User.objects.filter(last_login__lte=counted_date)
        unused_users_count = unused_users.count()
        unused_users.delete()

        # Find and delete old TmpImages, Feedbacks and Orders
        unused_temps = TmpImage.objects.filter(modified__lte=counted_date)
        unused_temps_count = unused_temps.count()
        unused_feedbacks = Feedback.objects.filter(modified__lte=counted_date)
        unused_feedbacks_count = unused_feedbacks.count()
        unused_orders = ProductOrder.objects.filter(modified__lte=counted_date)
        unused_orders_count = unused_orders.count()

        unused_temps.delete()
        unused_feedbacks.delete()
        unused_orders.delete()

        self.stdout.write(self.style.SUCCESS('Removed ' + str(unused_users_count) + ' user(s)'))
        self.stdout.write(self.style.SUCCESS('Removed ' + str(unused_temps_count) + ' tmp_image(s)'))
        self.stdout.write(self.style.SUCCESS('Removed ' + str(unused_feedbacks_count) + ' feedback(s)'))
        self.stdout.write(self.style.SUCCESS('Removed ' + str(unused_orders_count) + ' product_order(s)'))
        self.stdout.write(self.style.SUCCESS('Old data cleaned finished!'))
