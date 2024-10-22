from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User, Subscriptions


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="tester@mail.com")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="test subscribe",
            description="test description"
        )

    def test_subscription(self):
        """ Тест на оформление и удаление подписки """
        url = reverse('users:subscription', args=[self.course.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Подписка добавлена')
        self.assertEqual(Subscriptions.objects.all().count(), 1)
        self.assertTrue(self.course.subscribers.filter(user=self.user).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Подписка удалена')
        self.assertEqual(Subscriptions.objects.all().count(), 0)
        self.assertFalse(self.course.subscribers.filter(user=self.user).exists())