from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.conf import settings
from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_auth.registration.views import SocialLoginView
from rest_auth.utils import jwt_encode
from rest_auth.views import LoginView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import login as django_login

from member.serializers import UserLoginSerializer, FacebookLoginSerializer
from member.serializers.user_serializers import UserCreationSerializer, \
    PaginatedUserSerializer, UserSerializer

from ..models import User

__all__ = (
    'UserListView',
    'UserLoginView',
    'FacebookLoginView',
)

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = PaginatedUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserLoginView(LoginView):

    queryset = User.objects.all()
    permission_classes = (AllowAny, )
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


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = FacebookLoginSerializer




