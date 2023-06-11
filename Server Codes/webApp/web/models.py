from django.db import models
from django.utils import timezone
import datetime as dt


# Create your models here.
class userLog(models.Model):
    logID = models.CharField(max_length=60, unique=False, null=True)
    userName = models.CharField(max_length=70, blank=False, null=False)
    userID = models.CharField(max_length=20, blank=False, null=False)
    action = models.CharField(max_length=50, blank=False, null=False)
    dateTime = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.userName + ' | ' + str(self.dateTime)
