from django.urls import path, include

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('signout/', views.signout, name='signout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('profile/(?P<username>[-_\w.]+)/$', views.profile, name='profile'),
    path('profile/(?P<username>[-_\w.]+)/edit/$', views.profile_settings, name='profile_settings'),
    path('index/', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('user/<str:username>/follow/', views.FollowUser.as_view(), name='user_follow'),
]
