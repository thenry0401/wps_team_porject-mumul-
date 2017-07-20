from django.db import models

from config import settings
from post.models import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.base.AUTH_USER_MODEL)
    content = models.CharField(max_length=30, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
