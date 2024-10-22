from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.management.commands.bulk_create_courses import courses_data
from materials.management.commands.bulk_create_lessons import lessons_data
from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="tester@mail.com")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="test course",
            description="test course description"
        )
        self.lesson = Lesson.objects.create(
            owner=self.user,
            title="test lesson",
            description="test lesson description",
            link_to_video="https://www.youtube.com/watch?v=A3fCrmOC3q8",
            course=self.course
        )

    def test_list_lessons(self):
        """ Тест на получение списка уроков """
        url = reverse('materials:lessons')
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "owner": self.user.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "link_to_video": self.lesson.link_to_video,
                    "course": self.course.pk
                },
            ]
        }
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(response.json(), result)

    def test_delete_lesson(self):
        """ Тест на удаление урока """
        url = reverse('materials:delete_lesson', args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_update_lesson(self):
        """ Тест на изменение урока """
        url = reverse('materials:update_lesson', args=[self.lesson.pk])
        data = {
            "title": "title updated",
            "description": "description updated",
            "link_to_video": "https://www.youtube.com/watch?v=w0xaraSTVqY",
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['description'], data['description'])
        self.assertEqual(response.json()['link_to_video'], data['link_to_video'])

    def test_retrieve_lesson(self):
        """ Тест на получение урока """
        url = reverse('materials:lesson', args=[self.lesson.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['owner'], self.user.pk)
        self.assertEqual(response.json()['title'], self.lesson.title)
        self.assertEqual(response.json()['description'], self.lesson.description)
        self.assertEqual(response.json()['link_to_video'], self.lesson.link_to_video)

    def test_create_lesson(self):
        """ Тест на создание урока """
        url = reverse('materials:create_lesson')
        data = {
            "title": "test create lesson",
            "description": "test create description",
            "link_to_video": "https://www.youtube.com/watch?v=A3fCrmOC3q8",
            "course": self.course.pk
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['owner'], self.user.pk)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['description'], data['description'])
        self.assertEqual(response.json()['link_to_video'], data['link_to_video'])
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_create_lesson2(self):
        """ Тест на валидацию ссылки """
        url = reverse('materials:create_lesson')
        data = {
            "title": "test create lesson",
            "description": "test create description",
            "link_to_video": "https://www.vk.com/watch?v=A3fCrmOC3q8",
            "course": self.course.pk
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)
