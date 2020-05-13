from django.contrib import admin
from .models import UserProfile, Post, Follow, Rating, Comment

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Rating)
admin.site.register(Comment)

