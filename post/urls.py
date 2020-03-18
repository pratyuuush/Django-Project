from django.conf.urls import url

from . import views

urlpatterns = [
    url('create_post/', views.create_post, name='create_post'),
]