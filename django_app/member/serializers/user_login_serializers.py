import json

from allauth.account.auth_backends import AuthenticationBackend
from allauth.socialaccount.helpers import complete_social_login
from django.contrib.auth import authenticate, get_user_model
from requests import HTTPError, exceptions
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE
from django.conf import settings

__all__ = (
    'UserLoginSerializer',
    'FacebookLoginSerializer',
    'NaverLoginSerializer',
)

User = get_user_model()


# class UserLoginSerializer(LoginSerializer):
#     """장고 자체 회원가입 유저의 Login Serializer"""
#
#     # email = serializers.EmailField(required=True, allow_blank=True)
#     # password = serializers.CharField(style={'input_type': 'password'})
#
#     # rest-auth 내 LoginSerializer는 3가지 필드(username, email, password)를 제공합니다.
#     # username은 사용하지 않으므로 삭제합니다.
#
#     def get_fields(self):
#         fields = super(LoginSerializer, self).get_fields()
#         fields['email'] = fields['username']
#         del fields['username']
#         return fields
#
#     def validate(self, attrs):
#         attrs['username'] = attrs['email']
#         del attrs['email']
#         return super(LoginSerializer, self).validate(attrs)
#
#     def _validate_email(self, email, password):
#         user = None
#         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ email : ", email)
#         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ password : ", password)
#
#
#         if email and password:
#             user = authenticate(email=email, password=password)
#             print("@@@@@@@@@@@@@@@@@@@@@ user ; ", user)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise serializers.ValidationError(msg)
#
#         return user
#
#     # # email 필드와 password 필드에 대해 유효성 검사를 실시합니다. validate 부모 메서드를 그대로 복붙하고, username이 들어가는 부분은 모두 지워서 token값을 받아오게 했습니다.
#     def validate(self, attrs):
#         username = attrs.get('username')
#         email = attrs.get('email')
#         password = attrs.get('password')
#         print("@@@@@@@@@@@@@@ username ", username)
#         print("@@@@@@@@@@@@@@ email ", email)
#         print("@@@@@@@@@@@@@@ password ", password)
#
#
#         user = None
#
#         if 'allauth' in settings.INSTALLED_APPS:
#             from allauth.account import app_settings
#
#             # Authentication through email
#             if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
#                 user = self._validate_email(email, password)
#
#         else:
#             # Authentication without using allauth
#             if email:
#                 try:
#                     username = User.objects.get(email__iexact=email).get_username()
#                 except User.DoesNotExist:
#                     pass
#
#             if username:
#                 user = self._validate_username_email(username, '', password)
#
#         # Did we get back an active user?
#         if user:
#             if not user.is_active:
#                 msg = _('User account is disabled.')
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = _('Unable to log in with provided credentials.')
#             raise serializers.ValidationError(msg)
#
#         # If required, is the email verified?
#         if 'rest_auth.registration' in settings.INSTALLED_APPS:
#             from allauth.account import app_settings
#             if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
#                 email_address = user.emailaddress_set.get(email=user.email)
#                 if not email_address.verified:
#                     raise serializers.ValidationError(_('E-mail is not verified.'))
#
#         attrs['user'] = user
#         return attrs

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = AuthenticationBackend._authenticate_by_email(
                self=self,
                email=email,
                password=password,
            )

            if user:
                if not user.is_active:
                    msg = '유저의 계정이 비활성화 상태입니다'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'email, password가 일치하지 않습니다'
                raise serializers.ValidationError(msg)
        else:
            msg = '유저가 존재하지 않습니다'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        print(attrs['user'])
        return attrs


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

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()
        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        if attrs.get('access_token'):
            access_token = attrs.get('access_token')
        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            login.lookup()
            login.save(request, connect=True)
        attrs['user'] = login.account.user
        return attrs


class NaverLoginSerializer(SocialLoginSerializer):
    """네이버 로그인을 통한 Login Serializer"""
    pass
