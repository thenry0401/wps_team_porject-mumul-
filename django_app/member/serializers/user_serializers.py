import json

from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import LoginSerializer, UserModel
from rest_framework import serializers, pagination, exceptions
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import UniqueValidator

from config import settings
from config.settings.base import CONFIG_SECRET_DEPLOY_FILE
from ..models import User

__all__ = (
    'UserSerializer',
    'UserCreationSerializer',
    'UserLoginSerializer',
    'FacebookLoginSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        write_only_fields = ('password', )
        read_only_fields = ('id', )
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

    # rest-auth 내 LoginSerializer는 3가지 필드(username, email, password)를 제공합니다.
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username'] # username은 사용하지 않으므로 삭제합니다.
        return fields

    def validate(self, attrs):
        attrs['username'] = attrs['email']
        del attrs['email']
        return super(LoginSerializer, self).validate(attrs)


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