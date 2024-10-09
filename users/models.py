from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


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


class Payment(models.Model):
    method_payments = [
        ("transfer", "Денежный перевод"),
        ("cash", "Наличный расчет")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    paid_course = models.OneToOneField(Course, on_delete=models.SET_NULL, blank=True, null=True)
    # or
    paid_lesson = models.OneToOneField(Lesson, on_delete=models.SET_NULL, blank=True, null=True)

    date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    method = models.CharField(choices=method_payments, verbose_name="Способ оплаты")

    def __str__(self):
        product = self.paid_course if self.paid_course else self.paid_lesson
        return f"{self.date}: {self.user} купил {product}. {self.method} - {self.amount} руб."

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ('-date',)

