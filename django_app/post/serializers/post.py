from rest_framework import serializers

from ..models import Post

__all__ = (
    'PostSerializer',
    'PostInfoSerializer',
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
            'category',
            'trading_type',
            'post_code',
            'road_address',
            'detail_address',

            'like_users',
            'is_sold',
            'exchange_count',
            'created_date',
            'modified_date',
        )
        read_only_fields = (
            'author',
        )


class PostInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'photo',
            'content',
            'post_code',
            'road_address',
            'detail_address',
            'like_users',
            'is_sold',
            'exchange_count',
            'category',
            'trading_type',
        )
