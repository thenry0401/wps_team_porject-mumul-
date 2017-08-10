from rest_framework import serializers

from member.serializers import UserSerializer
from ..serializers.comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

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
            'comments',

            'like_users',
            'is_sold',
            'exchange_count',
            'created_date',
            'modified_date',
        )
        read_only_fields = (
            'author',
        )

