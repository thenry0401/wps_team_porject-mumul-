from rest_framework import serializers

from ..models import Post

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'photo',
            'content',
            'created_date',
            'modified_date',
            'post_code',
            'road_address',
            'detail_address',
            'like_users',
            'is_sold',
            'exchange_count',
            'category',
            'trading_type',
        )

