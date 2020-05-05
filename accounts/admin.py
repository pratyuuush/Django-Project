from django.contrib import admin
from .models import UserProfile, Post, Follow, Rating

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Rating)
