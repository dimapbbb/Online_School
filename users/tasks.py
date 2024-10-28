from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def check_users():
    users = User.objects.all()
    for user in users:

        if user.last_login:
            last_login = user.last_login.strftime('%d.%m.%Y')
            shutdown_threshold = (datetime.now() - timedelta(days=30)).strftime('%d.%m.%Y')

            if last_login > shutdown_threshold:
                user.is_active = False
                user.save()