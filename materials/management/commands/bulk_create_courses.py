from django.core.management import BaseCommand

from materials.models import Course


courses_data = [
    {
        "id": 2,
        "title": "backend",
        "description": "servers developer"
    },
    {
        "id": 3,
        "title": "frontend",
        "description": "web developer"
    },
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for data in courses_data:
            Course.objects.create(**data)
