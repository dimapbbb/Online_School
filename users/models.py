from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")

    phone = models.CharField(max_length=30, verbose_name="Номер телефона", blank=True, null=True)
    avatar = models.ImageField(upload_to='users_photo/', verbose_name="Аватар", blank=True, null=True)
    city = models.CharField(max_length=25, verbose_name="Страна", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
