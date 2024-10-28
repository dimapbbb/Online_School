from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course


@shared_task
def send_mail_of_update(pk):
    """ Отправляет сообщение всем подписчикам курса об обновлении """
    course = Course.objects.get(pk=pk)
    subscribers = list(course.subscribers.all())

    if subscribers:
        email_list = [subscribe.user.email for subscribe in subscribers]

        send_mail(
            subject="Получены обновления",
            message=f"Курс {course.title} обновлен, зайдите не сайт чтобы узнать больше",
            from_email=EMAIL_HOST_USER,
            recipient_list=email_list
        )