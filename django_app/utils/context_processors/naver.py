import json

from config import settings
from config.settings.base import CONFIG_SECRET_DEPLOY_FILE


def naver_login_api_info(request):
    config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())
    context = {
        'naver_app_id': config_secret_deploy['naver']['SOCIAL_AUTH_NAVER_KEY']
    }

    return context