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
        return attrs


class FacebookLoginSerializer(SocialLoginSerializer):
    """페이스북 로그인을 통한 Login Serializer"""
    # access token : EAAEDqblrwHUBACLFSfFEp56sY5nr5k67sylLQFuoK4Ycr3VwuLKcQc5gOtFnWGXiXQnuDfTp6ZCbHieJnDhKMImCZAp52GE7nASw2oZCyGFrlKT7lrtRtKEccubsmcOoJscepQaKZCPTyUhzCnlqfIg6bs35aQptFpVU6uSPJQZDZD
    # code : AQAl3yHRk-qsGch_iPGSveLRa8MNR3Y1FHV5keqh6nkCqOkdxQNDk1m8kJ3og2aVG4Cs_GI45JWlWNj4LodKldOytk-4k2lwJXqtE2H0inWLIUMz-sKdPfciIeCuhUCSihBui8r4fyuayXyChM42WkZqevp5CAg6elvqb17j26Rz2ypbtGKJllaT7QGF_7ko4M-0dq3srmTAnJezuvsh4D81k56hGgaamUnItVuUcMdhpgYiaLVpNhDSeOZiq0WEtMUGZaUD63FW0C3mSz0Yjcw7j9oQCDy0Kgcb61WbOPNo_iMZkti5EFD99MXW_ctYv61a4_uD8pOkJ96jpgSA1pUL
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
