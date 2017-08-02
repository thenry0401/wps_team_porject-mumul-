import json

from django.middleware.csrf import rotate_token, _get_new_csrf_string

from config import settings
from config.settings.base import CONFIG_SECRET_DEPLOY_FILE

__all__ = (
    'naver_login_api_info',
)

def naver_login_api_info(request):
    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())
    context = {
        'naver_app_id': config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_KEY']
    }

    return context
