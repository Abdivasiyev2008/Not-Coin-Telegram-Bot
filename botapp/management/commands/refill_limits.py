from django.core.management.base import BaseCommand
from django.utils import timezone
from botapp.models import User
from datetime import timedelta

class Command(BaseCommand):
    help = 'Refill user limits every 3 seconds'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        users = User.objects.all()
        for user in users:
            elapsed_time = (now - user.last_interaction).total_seconds()
            if user.limit < user.energy:
                user.limit = min(self.energy, self.limit + int(elapsed_time // 3))
                user.last_interaction = now
                user.save()

        self.stdout.write(self.style.SUCCESS('Successfully refilled limits'))
