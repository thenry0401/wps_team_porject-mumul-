import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        # email = options[self.User.USERNAME_FIELD]
        # password = None
        config_secret_common = json.loads(open(settings.SECRET_COMMON_JSON_FILE).read())
        username = config_secret_common['django']['default_superuser']['username']
        password = config_secret_common['django']['default_superuser']['password']

        # 슈퍼유저를 만드려고할때, 해당 username을 갖는 User가 없어야 한다.
        if not User.objects.filter(email=username).exists():
            User.objects.create_superuser(
                email=username,
                password=password,
            )
            print('Superuser %s is created' % username)
        else:
            print("Superuser %s is already exist" % username)