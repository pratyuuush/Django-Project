from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCreateForm, UserUpdateForm, PostForm
from .models import UserProfile, Post
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from annoying.decorators import ajax_request
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import datetime


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
    model = UserProfile
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
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        p_form = UserUpdateForm(instance=user.userprofile)

    context = {
        'user': user,
        'p_form': p_form
    }
    return render(request, 'accounts/profile_settings.html', context)


def index(request):
    if request.method == 'POST':
        p_form = PostForm(request.POST)
        if p_form.is_valid():
            post = Post(author=request.user.userprofile,
                          post_something=request.POST['post_something'],
                          posted_on=datetime.datetime.now(),
                          post_type = request.POST['post_type'],
                          )
            post.save()
           
            return redirect('index')
    else:
        p_form = PostForm()
    return render(request, 'accounts/index.html',{'p_form': p_form})   



@login_required(login_url='/login/')
class update_post(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required(login_url='/login/')
class DeletePost(UserPassesTestMixin, DeleteView):
    model = Post
    sucess_url = 'home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def settings(request):
    return render(request, 'accounts/settings.html')

class FollowUser(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, user=None, username=None):
        obj = get_object_or_404(User, username=username)
        prof_obj = get_object_or_404(UserProfile, user=obj)
        authenticated_user = self.request.user
        updated = False
        followed = False
        if authenticated_user.is_authenticated:
            if authenticated_user in prof_obj.followers.all():
                followed = False
                prof_obj.followers.remove(authenticated_user)
                follower_count = prof_obj.followers.count()
                button = 'Follow'
            else:
                followed = True
                prof_obj.followers.add(authenticated_user)
                follower_count = prof_obj.followers.count()
                button = 'Unfollow'
            updated = True
        data = {
            "updated": updated,
            "followed": followed,
            "follower_count": follower_count,
            "button": button
        }
        return Response(data)


class ViewFollowers(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'accounts/user_followers.html'
    context_object_name ='profile'
    ordering = ['-date_posted']

    def get_queryset(self):
        obj = get_object_or_404(User, username=self.kwargs.get('username'))
        prof_obj = get_object_or_404(UserProfile, user=obj)
        return prof_obj