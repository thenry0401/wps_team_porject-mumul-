from rest_framework import serializers

from post.models import Comment
from post.models import Post

__all__ = (
    'CommentSerializer',
    'MyPostsSerializer',
)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    my_posts = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'my_posts',
            'content',
            'created_date',
        )

        read_only_fields = (
            'author',
        )

    def get_my_posts(self, obj):
        post = Post.objects.filter(author=obj.author)
        serializer = MyPostsSerializer(post, many=True)
        return serializer.data


    def get_post(self, obj):
        return obj.post.title


class MyPostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'pk',
            'title',
            'photo',
        )