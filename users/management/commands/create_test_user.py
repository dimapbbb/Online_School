from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(email='test@mail.com')
        user.set_password('zxcdfrt56')
        user.save()
