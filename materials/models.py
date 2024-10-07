from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.FileField(upload_to="materials/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/", verbose_name="Превью")
    link_to_video = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
