from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post
from .utils import func_paginator

User = get_user_model()
POSTS_PAGE = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    page_obj = func_paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    template = 'posts/index.html'
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')[:POSTS_PAGE]
    page_obj = func_paginator(request, posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user_selected = get_object_or_404(User,
                                      username=username)
    posts = Post.objects.filter(author__username=username)
    post_count = posts.count()

    page_obj = func_paginator(request, posts)
    context = {
        'page_obj': page_obj,
        'user': user_selected,
        'author': user_selected,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    posts = Post.objects.filter(author__username=post.author)
    post_count = posts.count()

    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    context = {
        'form': form,
        'post': post, }
    if request.method == "POST":
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post_id)

    return render(request, 'posts/create_post.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', new_post.author)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)
