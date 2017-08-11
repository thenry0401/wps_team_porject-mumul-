from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.CustomBasicAuthentication import CustomBasicAuthenticationWithEmail
from post.models import Post, Comment
from post.serializers import CommentSerializer
from utils import ObjectIsRequestUser

__all__ = (
    'CommentListCreateView',
)


class CommentListCreateView(APIView):
    authentication_classes = (CustomBasicAuthenticationWithEmail,)
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
        serializer = CommentSerializer(post)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)