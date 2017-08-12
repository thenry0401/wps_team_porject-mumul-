import json

import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import \
    login as django_login, \
    logout as django_logout, \
    get_user_model

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE, AUTHENTICATION_BACKENDS
from member.forms import LoginForm

__all__ = (
    'login',
    'logout',
    'naver_login',
)

User = get_user_model()


def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user, backend=AUTHENTICATION_BACKENDS[0])
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


def naver_login(request):
    """
    base.html --> 네이버 로그인 창 --> 네이버 아이디로 로그인 --> 유저 정보(extra_data)와 함께 메인 페이지로 이동
    """
    access_token_url = "https://nid.naver.com/oauth2.0/token"
    profile_url = "https://openapi.naver.com/v1/nid/me"

    state = request.GET.get('state')
    code = request.GET.get('code')
    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

    print("@@@@ code : ", code)
    print("@@@@ state : ", state)

    class GetAccessTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]
            self.error = error_dict['error']
            self.error_description = error_dict['error_description']

    class DebugTokenException(Exception):
        def __init__(self, *args, **kwargs):
            """
            액세스 토큰 값에 error가 담겨서 오는 경우 예외를 발생시킵니다.
            :param args: ({'error': 'invalid_request', 'error_description': 'no valid data in session'}, )
            """
            error_dict = args[0]
            self.error = error_dict['error']
            self.error_description = error_dict['error_description']

    def add_message_and_redirect_referer():
        """
        # 네이버 로그인 오류 메시지를 request에 추가하고, 이전 페이지(base.html)로 redirect
        """
        # 유저용 메세지
        error_message_for_user = 'Naver login error'
        # request에 에러메세지를 전달
        messages.error(request, error_message_for_user)
        # 이전페이지로 redirect
        return redirect("index")

    def get_access_token(code, state):

        access_token_url_params = {
            'grant_type': "authorization_code",
            'client_id': config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_KEY'],
            'client_secret': config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_SECRET'],
            'code': code,
            'state': state,
        }

        # 파리미터를 조합해 만든 access_token_url로 GET 요청을 보냅니다.
        response = requests.get(access_token_url, params=access_token_url_params)

        # 네이버가 response 보내주는데, 이는 json 형식으로 출력이 가능합니다.
        result = response.json()

        if 'access_token' in result:
            # result값에서 액세스 토큰을 뽑아냅니다. 이를 가지고 유저 정보를 획득할 수 있습니다.
            access_token = result.get('access_token')
            print("금나와라 뚝딱 :", access_token)
            return access_token
        elif 'error' in result:
            raise GetAccessTokenException(result)
        else:
            raise Exception('Unknown error')

    def get_user_info(access_token):
        # 프로필 정보를 획득할 수 있는 URL에 액세스 토큰값을 헤더에 묻혀서 보냅니다.
        headers = {'Authorization': 'Bearer {0}'.format(access_token)}

        # 네이버는 유저 정보를 response로 던져줍니다.
        response = requests.get(profile_url, headers=headers)

        # 유저 정보를 dict 형식으로 만듭니다.
        extra_data = response.json().get('response')

        return extra_data

    if not code:
        return add_message_and_redirect_referer()

    try:
        access_token = get_access_token(code, state)
        extra_data = get_user_info(access_token)

        # Custom User Manager 내에 있는 메서드 get_or_create_naver_user를 활용해 유저를 가져옵니다.
        user = User.objects.get_or_create_naver_user(extra_data=extra_data)
        django_login(request, user, backend=AUTHENTICATION_BACKENDS[0])
        # for k, v in request.META.items():
        #     print(k, v)
        # return redirect(request.META['HTTP_REFERER'])
        return redirect('index')

    except GetAccessTokenException as e:
        print(e.error)
        print(e.error_description)
        return add_message_and_redirect_referer()

    except DebugTokenException as e:
        print(e.error)
        print(e.error_description)
        return add_message_and_redirect_referer()
