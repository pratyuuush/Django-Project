from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCreateForm, UserUpdateForm
from .models import UserProfile
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from .models import UserProfile
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()    
            UserProfile.objects.create(user=user, email = user.email)

            
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your Gigo account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/email_confirmation.html')
            login(request, new_user)
            return redirect('login')
    else:
         form = UserCreateForm()

    return render(request, 'accounts/register.html', {
        's_form': form
    })


def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')    
    
    return render(request, 'accounts/login.html', {
        'l_form': form
    })
    

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'accounts/email_confirmed.html')
    else:
        return render(request, 'accounts/email_not_confirmed.html')

def signout(request):
    logout(request)
    return redirect('home')


'''@login_required(login_url='/login/')'''


def home(request):
    return render(request, 'accounts/home.html')


def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    profile = UserProfile.objects.get(user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)        

    
def profile_settings(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('index')

    if request.method == 'POST':
        print(request.POST)
        p_form = UserUpdateForm(request.POST, instance=user.userprofile, files=request.FILES)
        if p_form.is_valid():
            p_form.save()
            return redirect(reverse('my_profile', kwargs={'username': user.username}))
    else:
        p_form = UserUpdateForm(instance=user.userprofile)

    context = {
        'user': user,
        'p_form': p_form
    }
    return render(request, 'accounts/profile_settings.html', context)

def followers(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    profiles = user_profile.followers.all

    context = {
        'header': 'Followers',
        'profiles': profiles,
    }

    return render(request, 'accounts/follow_list.html', context)


def following(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    profiles = user_profile.following.all

    context = {
        'header': 'Following',
        'profiles': profiles
    }
    return render(request, 'accounts/follow_list.html', context)
