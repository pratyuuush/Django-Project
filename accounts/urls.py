from django.urls import path, include
from django.contrib.auth import views as auth_views
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
    path('settings/', views.settings, name='settings'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change-password.html',
            success_url='/change-password-done'
        ),
        name='change_password'
    ),
    path('search/', views.search, name='search'),
    path('user/(?P<username>[-_\w.]+)/follows', views.FollowsListView.as_view(), name='user-follows'),
    path('user/(?P<username>[-_\w.]+)/followers', views.FollowersListView.as_view(), name='user-followers'),
]
