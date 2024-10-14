from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Владелец", blank=True, null=True)

    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.FileField(upload_to="materials/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Владелец", blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/", verbose_name="Превью")
    link_to_video = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
