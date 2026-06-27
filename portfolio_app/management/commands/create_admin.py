from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create the portfolio admin user'

    def handle(self, *args, **options):
        username = 'theara'
        password = 'portfolio2024'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email='', password=password)
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {username} / {password}'))
        else:
            self.stdout.write(f'Admin user "{username}" already exists.')