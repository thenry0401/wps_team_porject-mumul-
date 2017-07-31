import json

from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers, pagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE
from ..models import User

__all__ = (
    'UserSerializer',
    'UserCreationSerializer',
    'UserLoginSerializer',
    'FacebookLoginSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'nickname',
            'email',
            'user_type',
            'post_code', 'road_address', 'detail_address',
            'date_joined', 'last_login'
        )

class PaginatedUserSerializer(PageNumberPagination):
    """
    Serializes page objects of user querysets.
    """
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

    class Meta:
        object_serializer_class = UserSerializer


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=50,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("중복되는 아이디가 존재합니다.")
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')
        return data

    def save(self, *args, **wargs):
        user = User.objects.create_user(
            email=self.validated_data.get('email', ''),
            password=self.validated_data.get('password1', ''),
        )
        return user


class UserLoginSerializer(LoginSerializer):
    """장고 자체 회원가입 유저의 Login Serializer"""

    # rest-auth 내 LoginSerializer에서 일반 로그인은 email 필드를 제거
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['email']
        return fields


class FacebookLoginSerializer(SocialLoginSerializer):
    """페이스북 로그인을 통한 Login Serializer"""

    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())
    access_token = serializers.CharField(default=config_secret_deploy['facebook']['SOCIAL_AUTH_FACEBOOK_ACCESS_TOKEN'])
    # email = serializers.EmailField(required=False, allow_blank=True)
    # password = serializers.CharField(style={'input_type': 'password'})

    # def get_fields(self):
    #     fields = super(SocialLoginSerializer, self).get_fields()
    #     del fields['code']
    #
    #     return fields


class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None