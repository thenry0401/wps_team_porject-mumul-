from rest_framework import serializers

from ..serializers.comment import CommentSerializer
from ..models import Post

__all__ = [
    'PostSerializer',
    'PostSimpleInfoSerializer',
]

class PostSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
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

                'like_users',
                'is_sold',
                'exchange_count',
                'created_date',
                'modified_date',
            )

            read_only_fields = (
                'pk',
                'author',
            )

    def get_comments(self, obj):
        ordered_queryset = obj.comment_set.order_by('-pk')
        return CommentSerializer(ordered_queryset, many=True).data

class PostSimpleInfoSerializer(serializers.ModelSerializer):
    # SerializerMethodField는 메서드를 호출해 값을 얻어옵니다. get_<field_name> 메서드를 호출하게 됩니다.
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'photo',
            'content',
            'road_address',
            'detail_address',
            'comments',

            'like_users',
            'is_sold',
            'category',
            'trading_type',
        )

    def get_author(self, obj):
        # obj : <class 'post.models.post.Post'>
        post = Post.objects.get(pk=obj.pk)
        return post.author.nickname
