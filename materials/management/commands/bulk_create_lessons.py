from django.core.management import BaseCommand

from materials.models import Lesson


lessons_data = [
    {
        "id": 7,
        "course_id": 2,
        "owner_id": 3,
        "title": "django ORM",
        "description": "lesson_1",
        "link_to_video": "https://my.sky.pro/student-cabinet/stream-lesson/118646/theory/2"
    },
    {
        "id": 8,
        "course_id": 2,
        "owner_id": 3,
        "title": "FBV and CBV",
        "description": "lesson_2",
        "link_to_video": "https://my.sky.pro/student-cabinet/stream-lesson/118648/theory/1"
    },
    {
        "id": 9,
        "course_id": 3,
        "owner_id": 4,
        "title": "Html base",
        "description": "lesson_1",
        "link_to_video": "https://my.sky.pro/student-cabinet/stream-lesson/118648/theory/4"
    },
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for data in lessons_data:
            Lesson.objects.create(**data)