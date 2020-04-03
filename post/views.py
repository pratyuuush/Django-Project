from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
    )
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import UserPassesTestMixin    
from django.contrib.auth.decorators import login_required




def index(request):

    p_form = PostForm(request.POST)
    if request.method == 'POST':
        if p_form.is_valid():
            p_form.save(commit=True)
            return redirect('index')
    else:
        p_form = PostForm()
    return render(request, 'post/index.html',{'p_form': p_form})   



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