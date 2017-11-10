from django.shortcuts import get_object_or_404, redirect, render

from post.forms.comment import CommentForm
from post.models import Post, Comment

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
)


def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post:post_detail', post_pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'post/comment_modify.html', context)


def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    comment.delete()
    return redirect('post:post_detail', post_pk=post.pk)
