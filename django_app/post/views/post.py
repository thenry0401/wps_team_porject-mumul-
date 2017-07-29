from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from post.forms.post import PostForm

User = get_user_model()

__all__ = (
    'category_post_list',
    'hashtag_post_list',
    'location_post_list',
    'post_create',
    'post_delete',
    'post_detail',
    'post_like_toggle',
    'post_modify',
)


def category_post_list(request):
    pass


def hashtag_post_list(request):
    pass


def location_post_list(request):
    pass


def post_create(request):

    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(author=request.user)
        return redirect('post:post_create')

    else:
        form = PostForm(initial={'location' : request.user.road_address})
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request):
    pass


def post_modify(request):
    pass


def post_delete(request):
    pass


def post_like_toggle(request):
    pass





