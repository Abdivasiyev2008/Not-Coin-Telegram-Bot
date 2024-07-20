from django.db import models
from django.utils import timezone

class User(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    coins = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(auto_now=True)
    limit = models.IntegerField(default=1000)
    energy = models.IntegerField(default=1000)
    tap = models.IntegerField(default=1)
    sub = models.BooleanField(default=False)

    def refill_limit(self):
        now = timezone.now()
        elapsed_time = (now - self.last_interaction).total_seconds()
        if self.limit < self.energy:
            self.limit = min(self.energy, self.limit + int(elapsed_time // 3))

            self.last_interaction = now
            self.save()


    def __str__(self):
        return self.telegram_id