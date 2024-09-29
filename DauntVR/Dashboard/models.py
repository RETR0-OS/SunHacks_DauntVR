from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class GameEntry(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totalTime = models.FloatField(default=0)
    exposureTime = models.FloatField(default=0)
    sustainTime = models.FloatField(default=0)
    overcomeTime = models.FloatField(default=0)
    lookAwayTime = models.FloatField(default=0)
    levelCleared = models.BooleanField(default=False)
    report = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username