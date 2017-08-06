from allauth.account.utils import filter_users_by_email
from rest_framework.authentication import BasicAuthentication, get_authorization_header

import base64
import binascii

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions

User = get_user_model()

class CustomBasicAuthenticationWithEmail(BasicAuthentication):
    www_authenticate_realm = 'api'

    def _authenticate_by_email(self, **credentials):
        # Even though allauth will pass along `email`, other apps may
        # not respect this setting. For example, when using
        # django-tastypie basic authentication, the login is always
        # passed as `username`.  So let's place nice with other apps
        # and use username as fallback

        email = credentials.get('email', credentials.get('username'))
        if email:
            for user in filter_users_by_email(email):
                if user.check_password(credentials["password"]):
                    return user
        return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)  # 유저가 활성화 되었는지
        return is_active or is_active is None  # 유저가 없는 경우 is_active는 None이므로 True

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(userid, password)

    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            'password': password
        }

        # 수정한 부분
        user = self._authenticate_by_email(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm

