import json

from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE

__all__ = (
    'UserLoginSerializer',
    'FacebookLoginSerializer',
)


class UserLoginSerializer(LoginSerializer):
    """장고 자체 회원가입 유저의 Login Serializer"""

    # rest-auth 내 LoginSerializer는 3가지 필드(username, email, password)를 제공합니다.
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username']  # username은 사용하지 않으므로 삭제합니다.
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
