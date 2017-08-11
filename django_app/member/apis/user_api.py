from django.utils import timezone
from rest_auth.views import LoginView
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from member.CustomBasicAuthentication import CustomBasicAuthenticationWithEmail
from member.serializers import UserLoginSerializer
from member.serializers.user_serializers import PaginatedUserSerializer, UserSerializer, UserCreationSerializer
from post.models import Post, PostLike
from post.serializers.post import PostSimpleInfoSerializer
from utils.permissions import ObjectIsRequestUser

from ..models import User, Relation

__all__ = (
    'UserListView',
    'UserLoginView',
    'UserRetrieveUpdateDestroyView',

    'MyWishList',

    'PostLikeToggle',
    'UserFollowingToggle',
)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = PaginatedUserSerializer
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserLoginView(LoginView):
    # throttle_classes = ()
    # permission_classes = ()
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer, )
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=email)
        email.last_login = timezone.now()
        email.save(update_fields=['last_login'])
        return Response({'token': token.key})


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # 객체 하나를 가져와야 한다. 그런데 all()로 가져옴. 제네릭API뷰가 특정 오브젝트를 하나 들고온다.
    serializer_class = UserSerializer
    authentication_classes = (CustomBasicAuthenticationWithEmail,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object_user(self, pk):
        """
        /api/member/<유저 pk> 로 접근했을 때 해당 user를 리턴해주는 GenericAPIView의 유용한 메서드입니다.
        """
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:  # pk로 찾는 유저가 없을 때 404 Error를 띄웁니다.
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # update
    def put(self, request, pk):
        user = self.get_object_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # partial update
    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyWishList(generics.ListAPIView):
    authentication_classes = (CustomBasicAuthenticationWithEmail,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )
    serializer_class = PostSimpleInfoSerializer
    pagination_class = PaginatedUserSerializer

    def get_queryset(self):
        user = self.request.user
        items = Post.objects.filter(like_users=user.pk)
        return items.all()


class PostLikeToggle(APIView):
    authentication_classes = (CustomBasicAuthenticationWithEmail,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get(self, request, pk):
        user = User.objects.get(id=request.user.id)
        try:
            post = Post.objects.get(pk=pk)
            if post.author != user:
                # flat=True will remove the tuples and return the list
                if post.pk in user.my_wishlist.values_list('post', flat=True):
                    wishlist = PostLike.objects.filter(user=user, post=post)
                    wishlist.delete()
                    return Response(status=status.HTTP_200_OK,
                                    data={'detail': '매물 [{}]이(가) wishlist에서 삭제되었습니다.'.format(post.title)})
                else:
                    PostLike.objects.create(user=user, post=post)
                    return Response(status=status.HTTP_201_CREATED,
                                    data={'detail': '매물 [{}]이(가) wishlist에 추가되었습니다.'.format(post.title)})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': '본인의 매물을 위시리스트에 담을 수 없습니다.'})
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': '해당 매물을 찾을 수 없습니다.'})


class UserFollowingToggle(APIView):
    authentication_classes = (CustomBasicAuthenticationWithEmail,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get(self, request, user_pk):
        user = User.objects.get(pk=request.user.id)
        try:
            target_user = User.objects.get(pk=user_pk)
            if user.pk != target_user.pk:
                if user.is_follow(target_user):
                    Relation.objects.get(from_user=user.pk, to_user=target_user.pk).delete()
                    return Response(status=status.HTTP_200_OK,
                                    data={'detail': '[{from_user}]이(가) [{to_user}]를 언팔로잉 했습니다.'.format(
                                        from_user=user.nickname, to_user=target_user.nickname)}
                                    )
                else:
                    user.follow_toggle(target_user)
                    return Response(status=status.HTTP_201_CREATED,
                                    data={'detail': '[{from_user}]이(가) [{to_user}]를 팔로잉 하기 시작했습니다.'.format(
                                        from_user=user.nickname, to_user=target_user.nickname)}
                                    )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': '본인이 본인을 팔로잉할 수 없습니다.'})
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': '해당 유저를 찾을 수 없습니다.'})
