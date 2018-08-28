from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from member.models import User
from post.models.others import Tag
from post.models.post import Exchange
from utils import ObjectIsRequestUser
from ..serializers import PostSerializer
from ..models import Post, Comment

__all__ = (
    'PostListView',
    'PostCreateView',
    'PostDetailView',
    'PostModifyDeleteView',
    'PostLikeToggleView',
    'HashtagPostListView',
    'ForSaleToggleView',
    'MatchingItemsView',

    'SwaggerSchemaView',

)


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(for_sale=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly
    )

    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostModifyDeleteView(APIView):
    # IsAuthenticatedOrReadOnly 는 로그인 사용자에게만 write/update 권한을 주고
    # 로그인 안한 사용자에게는 read권한만 준다
    # ObjectIsRequestUser 는 로그인한 유저가 작성자와 일치하는지를 확인한다
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": '게시물을 찾을 수 없습니다.'})

    def put(self, request, post_pk):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = self.get_object(post_pk)
        post.delete()
        return Response({"status": status.HTTP_204_NO_CONTENT, "message": '삭제되었습니다.'})


class PostLikeToggleView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        if post.author_id != request.user.id:
            post_like, post_like_created = post.postlike_set.get_or_create(
                user=request.user
            )
            if not post_like_created:
                post_like.delete()
            if post_like_created:
                return Response('위시리스트에 추가 되었습니다.')
            else:
                return Response('위시리스트에서 제거되었습니다.')
        else:
            return Response('나의 게시물입니다')


class HashtagPostListView(APIView):
    def get_object(self, tag_name):
        try:
            return Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, tag_name):
        tag = self.get_object(tag_name)
        posts = Post.objects.filter(comment__tags=tag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class ForSaleToggleView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Http404

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        if post.author_id == request.user.id:
            post.make_for_sale()
            if post.for_sale:
                return Response('매물이 등록되었습니다.')
            else:
                return Response('매물이 해제되었습니다.')
        else:
            return Response('내가 등록한 게시물이 아닙니다')


class MatchingItemsView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_post_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Http404

    def get_comment_object(self, comment_pk):
        try:
            return Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            return Http404

    def post(self, request, post_pk, comment_pk):
        post_item = self.get_post_object(post_pk)
        comment_item = self.get_comment_object(comment_pk)
        exchange = Exchange.objects.create(
            post_item=post_item,
            comment_item=comment_item,
        )
        exchange.save()


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)
