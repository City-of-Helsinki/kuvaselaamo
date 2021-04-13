# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from clean_unused_data import DEFAULT_DAYS_UNTIL_NOTIFICATION
from django.core.mail import send_mail
from django.conf import settings

NOTIFICATION_SUBJECT = u"Helsinkikuvia.fi: Käyttäjätunnuksesi poistetaan pian"
NOTIFICATION_MESSAGE = u"""Hei! Et ole kirjautunut Helsinkikuvia.fi -palveluun pitkään aikaan. Käyttäjätunnuksesi ja siihen liittyvät tiedot poistetaan palvelusta 30 päivän kuluttua.

Jos haluat jatkaa palvelun käyttöä ja säilyttää tietosi, käy kirjautumassa osoitteessa https://helsinkikuvia.fi.

Helsinkikuvia.fi – helsinkiläisten kuva-aarre verkossa"""


class Command(BaseCommand):
    help = "Send an email notification to those users whose account will be removed shortly because of inactivity."

    def add_arguments(self, parser):
        parser.add_argument(
            "-dn", "--days_until_notification", type=int,
            help="Specifies the time in days after which a notification warning about removal will be sent to users.",
            default=DEFAULT_DAYS_UNTIL_NOTIFICATION
        )

    def handle(self, *args, **kwargs):
        days_until_notification = kwargs['days_until_notification']

        if days_until_notification < 0:
            self.stdout.write(self.style.ERROR(
                "Invalid parameters given. Ensure that days_until_notification is a positive integer."))
            return

        self.stdout.write(
            "Starting to send notifications to users whose accounts are about to be removed. Sending "
            "notifications to users whose last login date is older than %d days." % days_until_notification)

        counted_date = timezone.now() - timedelta(days=days_until_notification)
        users = User.objects.filter(last_login__lte=counted_date, is_superuser=False, is_staff=False,
                                    profile__is_museum=False, profile__is_admin=False,
                                    profile__removal_notification_sent__isnull=True)

        for user in users:
            send_mail(NOTIFICATION_SUBJECT, NOTIFICATION_MESSAGE, settings.DEFAULT_FROM_EMAIL, [user.email],
                      fail_silently=False)
            user.profile.removal_notification_sent = timezone.now()
            user.profile.save()

        self.stdout.write(
            self.style.SUCCESS('Removal notification sending finished, %d notifications sent!' % len(users)))
