from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.models import TokenModel
from rest_auth.registration.views import SocialLoginView
from rest_auth.views import LoginView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from member.serializers import UserSerializer
from member.serializers.user_serializers import UserCreationSerializer, UserLoginSerializer, FacebookLoginSerializer
from ..models import User

__all__ = (
    'UserListCreateView',
    'UserLoginView',
    'FacebookLoginView',
)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer

class UserLoginView(LoginView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    token_model = TokenModel

    def login(self):
        super(UserLoginView, self).login(self)


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = FacebookLoginSerializer




