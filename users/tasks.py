from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_users():
    users = User.objects.all()
    for user in users:

        if user.last_login:
            dt_now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())

            if user.last_login > dt_now - timedelta(days=30):
                user.is_active = False
                user.save()