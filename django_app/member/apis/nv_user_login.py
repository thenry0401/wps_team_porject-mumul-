from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from member.serializers import NaverLoginSerializer

__all__ = (
    'NaverLogin',
)


class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    serializer_class = NaverLoginSerializer
