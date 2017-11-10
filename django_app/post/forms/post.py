from django import forms

from post.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'photo',
            'post_code',
            'road_address',
            'detail_address',
            'category',
            'trading_type',
        ]

    def save(self, **kwargs):
        post = super().save(commit=False)
        post.author = kwargs.get('author', None)
        post.save()

        return post