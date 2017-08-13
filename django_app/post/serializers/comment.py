from rest_framework import serializers

from post.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'content',
            'created_date',
        )

        read_only_fields = (
            'post',
            'author',
        )

    def get_post(self, obj):
        return obj.post.title