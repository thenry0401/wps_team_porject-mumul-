from django.conf import settings
from django.db import models

from post.models import Post
from post.models.others import Tag

__all__ = (
    'Comment',
)


# 내가 가지고 있는걸 보여줘야됨
# 기본적인 코멘트 기능

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=30, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)



