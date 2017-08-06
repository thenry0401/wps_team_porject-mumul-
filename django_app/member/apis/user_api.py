from allauth.account.auth_backends import AuthenticationBackend
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_auth.registration.views import SocialLoginView
from rest_auth.utils import jwt_encode
from rest_auth.views import LoginView
from rest_framework import generics, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from member.serializers import UserLoginSerializer, FacebookLoginSerializer, UserFastCreationSerializer
from member.serializers.user_login_serializers import NaverLoginSerializer
from member.serializers.user_serializers import PaginatedUserSerializer, UserSerializer, UserCreationSerializer
from utils.permissions import ObjectIsRequestUser

from ..models import User

__all__ = (
    'UserListView',
    'UserLoginView',
    'UserCreateView',
    'FacebookLoginView',
    'NaverLoginView',
    'UserRetrieveUpdateDestroyView',
)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = PaginatedUserSerializer
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserFastCreationSerializer


class UserLoginView(LoginView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    token_model = TokenModel

    def login(self):
        self.user = self.serializer.validated_data['user']
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()


class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # 객체 하나를 가져와야 한다. 그런데 all()로 가져옴. 제네릭API뷰가 특정 오브젝트를 하나 들고온다.
    serializer_class = UserSerializer
    # authentication_classes = (CustomBasicAuthenticationWithEmail,)
    authentication_classes = (BasicAuthentication, SessionAuthentication, )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(pk):
        # /api/member/<유저 pk> 로 접근했을 때 해당 user를 리턴해주는 유용한 GenericAPIView의 메서드입니다.
        try:
            user = super().get_object()
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        print("@@@@@@@@@@@ GET 이건뭐지 : ", request)
        print("@@@@@@@@@@@ GET 이건뭐지 args: ", args)
        print("@@@@@@@@@@@ GET 이건뭐지 kwargs: ", kwargs)
        return self.retrieve(request, *args, **kwargs)

    # update
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, request, partial=True)
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
        print("@@@@ request :", request)
        print("@@@@ pk :", pk)
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = FacebookLoginSerializer


class NaverLoginView(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    serializer_class = NaverLoginSerializer
