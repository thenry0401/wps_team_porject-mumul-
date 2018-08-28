from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, Comment
from post.serializers import CommentSerializer
from utils import ObjectIsRequestUser

__all__ = (
    'CommentCreateView',
    'CommentModifyDeleteView',
)


class CommentCreateView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, post_pk):
        post = self.get_object(post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                post=post,
                author=request.user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentModifyDeleteView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk, comment_pk):
        try:
            return Comment.objects.get(post_id=post_pk, pk=comment_pk)
        except:
            raise Http404

    def put(self, request, post_pk, comment_pk):
        comment = self.get_object(post_pk, comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, comment_pk):
        comment = self.get_object(post_pk, comment_pk)
        comment.delete()
        return Response({"status": status.HTTP_204_NO_CONTENT, "message": '삭제되었습니다.'})
