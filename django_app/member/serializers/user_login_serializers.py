import json

from allauth import exceptions
from allauth.socialaccount.helpers import complete_social_login
from requests import HTTPError
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


class UserLoginSerializer(LoginSerializer):
    """장고 자체 회원가입 유저의 Login Serializer"""

    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    # rest-auth 내 LoginSerializer는 3가지 필드(username, email, password)를 제공합니다.
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username']  # username은 사용하지 않으므로 삭제합니다.
        return fields


    # email 필드와 password 필드에 대해 유효성 검사를 실시합니다. validate 부모 메서드를 그대로 복붙하고, username이 들어가는 부분은 모두 지워서 token값을 받아오게 했습니다.
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email (이메일을 통한 인증)
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
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
