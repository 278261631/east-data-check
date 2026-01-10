from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Create admin user from .env config'

    def handle(self, *args, **options):
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD
        email = settings.ADMIN_EMAIL

        if not username or not password:
            self.stdout.write(self.style.WARNING('ADMIN_USERNAME or ADMIN_PASSWORD not set in .env'))
            return

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" updated'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created'))

