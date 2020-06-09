from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

import random
import string


class Command(BaseCommand):
    help = "Add admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--username", type=str, help="Username", default="admin"
        )
        parser.add_argument(
            "-p", "--password", type=str, help="Password", default=""
        )
        parser.add_argument(
            "-e", "--email", type=str, help="Email", default="admin@example.com"
        )

    def handle(self, *args, **kwargs):
        if not get_user_model().objects.filter(username=kwargs["username"]).count():
            password = kwargs["password"]
            if not password:
                password = self.random_string(20)
                self.stdout.write(self.style.WARNING("Generated admin password " + password))
                self.stdout.write(self.style.WARNING("You should probably go and change it."))

            get_user_model().objects.create_superuser(
                kwargs["username"], kwargs["email"], password
            )

            self.stdout.write(self.style.SUCCESS("Created admin user " + kwargs["username"]))
        else:
            self.stdout.write("Admin user " + kwargs["username"] + " already exists, no need to create.")

    def random_string(self, len):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(len))