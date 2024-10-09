from django.core.management import BaseCommand

from users.models import User


users_data = [
    {
        "email": "test1@mail.com",
        "phone": "89871234567",
        "city": "Москва"
    },
    {
        "email": "test2@mail.com",
        "phone": "89872345678",
        "city": "Казань"
    },
    {
        "email": "test3@mail.com",
        "phone": "89873456789",
        "city": "Санкт-Петербург"
    },
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for data in users_data:
            user = User.objects.create(**data)
            user.set_password('zxcdfrt56')
            user.save()
