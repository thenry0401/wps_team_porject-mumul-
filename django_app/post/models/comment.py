import re
from audioop import reverse

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
    # my_posts = models.ForeignKey(Post, related_name='my_posts', blank=True, null=True)
    content = models.CharField(max_length=30, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    html_content = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    def make_html_content_and_add_tags(self):
        p = re.compile(r'(#\w+)')
        tag_name_list = re.findall(p, self.content)
        ori_content = self.content
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            change_tag = '<a href="">{}</a>'.format(tag_name)
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        self.html_content = ori_content
        super().save(update_fields=['html_content'])