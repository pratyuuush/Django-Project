from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCreateForm, UserUpdateForm, PostForm
from .models import UserProfile, Post, Follow
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
from django.apps import apps


PAGINATION_COUNT = 5

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


def explore(request):
    random_posts = Post.objects.all().order_by('?')[:40]
    queryset = None
    query = request.GET.get('q')
    if query:
        if query.startswith('#'):
            queryset = Post.objects.all().filter(
                Q(caption__icontains=query)
                ).distinct()
        else:
            Profile = apps.get_model('accounts', 'UserProfile')
            queryset = UserProfile.objects.all().filter(
                Q(user__username__icontains=query)
                ).distinct()

    context = {
        'searches': queryset,
        'posts': random_posts
    }
    return render(request, 'accounts/explore.html', context)



def profile(request, username):
    visible_user = User.objects.get(username=username)
    visible_user_id = visible_user.id
    user = visible_user.userprofile

    if not visible_user:
        return redirect('index')

    logged_user = request.user
    logged_user_id = request.user.id


    follows_between=Follow.objects.filter(user=logged_user_id,
                                        follow_user=visible_user_id)

    if 'follow' in request.POST:
        new_relation = Follow(user=logged_user, follow_user=visible_user)
        if follows_between.count() == 0:
            new_relation.save()
    elif 'unfollow' in request.POST:
        if follows_between.count() > 0:
            follows_between.delete()
    
    if logged_user is None:
        can_follow = False
    else:
        can_follow = (Follow.objects.filter(user=logged_user_id,
                                                follow_user=visible_user_id).count() == 0)

    ordering = ['-posted_on']
    paginate_by = PAGINATION_COUNT

    posts = Post.objects.filter(author=user).order_by('-posted_on')  

    context = {
        'username': username,
        'user': visible_user,
        'profile': profile,
        'logged_user': logged_user,
        'can_follow': can_follow,
        'posts':posts
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


    paginate_by = PAGINATION_COUNT

    user = request.user
    userprofile = request.user.userprofile
    qs = Follow.objects.filter(user=user)
    follows = [userprofile]
    for obj in qs:
        follows.append(obj.follow_user.userprofile)
    
        
    posts = Post.objects.filter(author__in=follows).order_by('-posted_on')

    
    context = {
    'p_form': p_form,
    'posts':posts
    }   
    return render(request, 'accounts/index.html',context)   



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




def search(request):
    queryset = None
    query = request.GET.get('q')
    if query:
        if query.startswith('#'):
            queryset = Post.objects.all().filter(
                Q(caption__icontains=query)
                ).distinct()
        else:
            Profile = apps.get_model('accounts', 'UserProfile')
            queryset = UserProfile.objects.all().filter(
                Q(user__username__icontains=query)
                ).distinct()

    context = {
        'posts': queryset
    }
    return render(request, "accounts/search.html", context)


class FollowsListView(ListView):
    model = Follow
    template_name = 'accounts/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'accounts/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data
     
     