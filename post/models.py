from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfile
from datetime import datetime

# Create your models here.


class Post(models.Model):
    caption = models.TextField(max_length=2000, null=True, blank=True)
    posted_on = models.DateTimeField(default=datetime.now)

    user_profile = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    def save(self, **kwargs):
        super().save()

