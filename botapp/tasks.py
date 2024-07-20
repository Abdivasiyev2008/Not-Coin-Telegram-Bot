from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import User

@shared_task
def refill_limits():
    users = User.objects.all()
    for user in users:
        if user.limit < user.energy:
            user.limit += 1
            user.save()
