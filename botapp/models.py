from django.db import models
from django.utils import timezone


class UserManager(models.Manager):
    def get(self, *args, **kwargs):
        instance = super().get(*args, **kwargs)
        instance.refill_limit()
        return instance


class User(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    coins = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(auto_now=True)
    limit = models.IntegerField(default=1000)
    energy = models.IntegerField(default=1000)
    tap = models.IntegerField(default=1)
    sub = models.BooleanField(default=False)

    objects = UserManager()

    def refill_limit(self):
        now = timezone.now()
        elapsed_time = (now - self.last_interaction).total_seconds()

        if self.limit < self.energy:
            # Calculate the number of refill intervals that have passed
            refill_intervals = int(elapsed_time // 3)
            if refill_intervals > 0:
                # Increase limit by refill_intervals, but not exceeding energy
                self.limit = min(self.energy, self.limit + refill_intervals * 5)
                # Update last interaction time to the current time
                self.last_interaction = now
                self.save()
                return self.limit


    def __str__(self):
        return self.telegram_id


class RefFriendModel(models.Model):
    telegram_id = models.CharField(max_length=255)
    ref_friend = models.CharField(max_length=255)

    def __str__(self):
        return self.telegram_id
