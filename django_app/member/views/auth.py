import json

import requests

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth import \
    login as django_login, \
    logout as django_logout, get_user_model

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE
from member.forms import LoginForm

__all__ = (
    'login',
    'logout',
    'naver_login',
    'SocialAccountAdapter',
)

User = get_user_model()


def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('index')

    else:
        if request.user.is_authenticated:
            return redirect("index")

        form = LoginForm()
    context = {
        'form': form
    }

    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('index')


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        allauth를 통해서 유저를 저장할 때 호출됩니다. 유저 객체에 추가적인 정보를 담기 위해서 오버라이드를 실시했습니다.
        """

        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        # (하드코딩) social_app_name = str(request.path).split("/")[2].upper()
        social_app_name = sociallogin.account.provider.upper()
        extra_data = sociallogin.account.extra_data

        if social_app_name == "FACEBOOK":
            profile_url = "https://graph.facebook.com/v2.4/{user_id}/picture?type=square&height={height}&width={width}&return_ssl_rources=1".format(
                user_id=extra_data['id'],
                height=150,
                width=150,
            )
            User.objects.get_or_create_facebook_user(user_pk=user.pk, extra_data=extra_data, profile_url=profile_url)

        elif social_app_name == "NAVER":
            User.objects.get_or_create_naver_user(user_pk=user.pk, extra_data=extra_data)

        return user


def naver_login(request):
    """ base.html에서 네이버 아이디로 로그인을 거친 후, 이 함수에 request가 들어오게 됩니다. """
    state = request.GET.get('state')
    code = request.GET.get('code')
    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

    # print("@@@@@@@@@@@@@@@@@@@@@@ state : ", state)
    # print("@@@@@@@@@@@@@@@@@@@@@@ code : ", code)

    def get_access_token(code):
        """
        request로부터 code를 받아 액세스토큰 교환 URL에 요청, 이후 해당 액세스 토큰을 반환
        """
        # 액세스 토큰 발급 요청 URL을 의미합니다.
        access_token_url = "https://nid.naver.com/oauth2.0/token" \
                           "?grant_type=authorization_code" \
                           "&client_id={client_id}" \
                           "&client_secret={client_secret}" \
                           "&code={code}" \
                           "&state={state}".format(
                                            client_id=config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_KEY'],
                                            client_secret=config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_SECRET'],
                                            code=code,
                                            state=state,
                                            )

        response = requests.get(access_token_url)
        result = response.json()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ response : ", response)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ result : ", result)

        if 'access_token' in result:
            return result['access_token']

    result = get_access_token(code)
    context = {
        'result' : result
    }
    return render(request, 'member/test.html', context)
