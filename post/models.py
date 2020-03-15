from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    caption = models.TextField(max_length=2200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    location = models.CharField(max_length=30, blank=True)

    def save(self, **kwargs):
        super().save()
