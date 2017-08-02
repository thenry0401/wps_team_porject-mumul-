from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from post.forms.post import PostForm
from post.models import Post

User = get_user_model()

__all__ = (
    'post_list',
    'post_search_result',
    'post_create',
    'post_delete',
    'post_detail',
    'post_like_toggle',
    'post_modify',
)


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_search_result(request):
    context = {

    }
    return render(request, 'post/search_result.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm(initial={'location': request.user.road_address})
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post
    }
    return render(request, 'post/post_detail.html', context)


def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:post_list')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    else:
        context = {
            'post': post,
        }
        return render(request, 'post/post_delete.html', context)


def post_like_toggle(request, post_pk):
    pass
