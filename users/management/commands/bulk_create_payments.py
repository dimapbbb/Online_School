from django.core.management import BaseCommand

from users.models import Payment


payments_data = [
    {
        "user_id": 2,
        "paid_course_id": 2,
        "amount": 50000,
        "method": "transfer"
    },
    {
        "user_id": 3,
        "paid_course_id": 3,
        "amount": 40000,
        "method": "transfer"
    },
    {
        "user_id": 4,
        "paid_lesson_id": 7,
        "amount": 10000,
        "method": "cash"
    },
    {
        "user_id": 2,
        "paid_lesson_id": 9,
        "amount": 12000,
        "method": "transfer"
    },
    {
        "user_id": 4,
        "paid_lesson_id": 8,
        "amount": 13000,
        "method": "cash"
    },
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for data in payments_data:
            Payment.objects.create(**data)
