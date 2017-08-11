from rest_framework import serializers

from member.serializers import UserSerializer
from ..serializers.comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer',
    'PostInfoSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

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

    def get_comments(self, obj):
        ordered_queryset = obj.comment_set.order_by('-pk')
        return CommentSerializer(ordered_queryset, many=True).data


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

