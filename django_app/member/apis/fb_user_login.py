from allauth.socialaccount.providers.facebook.provider import FacebookProvider, GRAPH_API_URL
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter, fb_complete_login, \
    compute_appsecret_proof
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from requests import request
from rest_auth.registration.views import SocialLoginView
import requests
from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from allauth.socialaccount import providers

from member.serializers import FacebookLoginSerializer

__all__ = (
    'FacebookLogin',
    'CustomFacebookOAuth2Adapter',
    'FacebookLogin',
)

User = get_user_model()

def fb_profile_image_url_save(login):
    profile_url = "https://graph.facebook.com/v2.4/{user_id}/picture" \
                  "?type=square&height={height}&width={width}" \
                  "&return_ssl_rources=1".format(
                        user_id=login.user,
                        height=150,
                        width=150,
                    )
    temp_file = NamedTemporaryFile(delete=False)  # 임시 파일을 하나 생성
    response = request('GET', profile_url, params={'type': 'large'})
    response.raise_for_status()
    temp_file.write(response.content)

    try:
        login.user.profile_image.save('{0}_{1}.jpg'.format(login.user, login.user.get_full_name()), File(temp_file))
    except IntegrityError as IE:
        print(IE)

    return login.user.profile_image

def fb_complete_login(request, app, token):
    provider = providers.registry.by_id(FacebookProvider.id, request)
    resp = requests.get(
        GRAPH_API_URL + '/me',
        params={
            'fields': ','.join(provider.get_fields()),
            'access_token': token.token,
            'appsecret_proof': compute_appsecret_proof(app, token)
        })
    resp.raise_for_status()
    extra_data = resp.json()
    login = provider.sociallogin_from_response(request, extra_data)
    # 유저 닉네임 변경
    login.user.nickname = extra_data['id']

    # 유저 타입 변경
    login.user.user_type = 'F'

    # 프로필 이미지 저장
    login.user.profile_image = fb_profile_image_url_save(login)

    return login


class CustomFacebookOAuth2Adapter(FacebookOAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return fb_complete_login(request, app, access_token)


class FacebookLogin(SocialLoginView):
    adapter_class = CustomFacebookOAuth2Adapter
    serializer_class = FacebookLoginSerializer
