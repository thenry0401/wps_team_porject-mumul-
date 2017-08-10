from rest_framework import serializers

from post.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'content',
            'created_date',
        )