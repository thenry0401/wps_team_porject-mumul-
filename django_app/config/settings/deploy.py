# deploy.py
from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'

# (170705) AWS S3 settings
AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret_deploy['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = config_secret_deploy['aws']['s3_region_name']
S3_USE_SIG4 = True  # AWS_S3_SIGNATURE_VERSION = config_secret_deploy['aws']['s3_signature_version']

# Storage settings
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = '.media'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'   # 기본 스토리지
STATICFILES_STORAGE = 'config.storages.StaticStorage'   # 이 두 줄을 작성하고 나면 static root, .media root 줄은 필요 없어진다.

# .media
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
MEDIA_URL = "/.media/"
# MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# 배포모드니까 DEBUG는 False
DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# Database
DATABASES = config_secret_deploy['django']['databases']



print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)
