from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = options[self.User.USERNAME_FIELD]
        password = None
        # 슈퍼유저를 만드려고할때, 해당 username을 갖는 User가 없어야 한다.
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
            )
            print('Superuser %s is created' % email)
        else:
            print("Superuser %s is already exist" % email)