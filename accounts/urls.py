from django.conf.urls import url

from . import views

urlpatterns = [
    url('home/', views.home, name='index'),
    url('register/', views.register, name='register'),
    url('login/', views.login_user, name='login'),
    url('signout/', views.signout, name='signout'),
]
