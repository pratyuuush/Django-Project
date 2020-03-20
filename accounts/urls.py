from django.conf.urls import url

from . import views

urlpatterns = [
    url('home/', views.home, name='home'),
    url('register/', views.register, name='register'),
    url('login/', views.login_user, name='login'),
    url('index/', views.index, name='index'),
    url('signout/', views.signout, name='signout'),
]
