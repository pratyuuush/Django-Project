from django.contrib import admin
from .models import UserProfile, Post

admin.site.register(Post)
admin.site.register(UserProfile)

