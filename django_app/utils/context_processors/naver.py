import json

from django.template.defaultfilters import urlencode

from config.settings.base import CONFIG_SECRET_DEPLOY_FILE

__all__ = (
    'naver_login_api_info',
)

def naver_login_api_info(request):
    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

    urlencode_redirect_uri = urlencode("http://localhost:8000/member/naver-login")

    context = {
        'naver_app_id': config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_KEY'],
        'urlencode_redirect_uri': urlencode_redirect_uri
    }

    return context
