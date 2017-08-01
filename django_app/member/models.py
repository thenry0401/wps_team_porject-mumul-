from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.db import models

# Create your models here.
from requests import request, HTTPError

from utils.fields.custom_imagefield import CustomImageField


class UserManager(DefaultUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email, password=password, nickname=nickname)
        user.email = email
        user.nickname = nickname
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


    # 페이스북으로 가입하면 user_type을 F(Facebook)으로 지정한다.
    def get_or_create_facebook_user(self, user_pk, extra_data, profile_url):
        print(extra_data)
        user = User.objects.get(pk=user_pk)
        user.nickname = str(user.id) + str(user.nickname)
        user.user_type = user.USER_TYPE_FACEBOOK
        user.profile_image = profile_url

        # 프로필 이미지를 저장합니다.
        try:
            response = request('GET', profile_url, params={'type' : 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            temp_file = NamedTemporaryFile(delete=False) # 임시 파일을 하나 생성
            user.profile_image.save('{0}_{1}_social_facebook.jpg'.format(extra_data['id'], user.username), ContentFile(response.content))
            temp_file.write(response.content)

        user.save()

        return user

    # 네이버로 가입하면 user_type을 N(Naver)으로 지정한다. 그외에 추가적인 정보를 커스텀 저장을 한다.
    def get_or_create_naver_user(self, user_pk, extra_data):
        print(extra_data)
        user = User.objects.get(pk=user_pk)
        user.email = extra_data['email']
        user.name = extra_data['name']
        user.profile_image = extra_data['profile_image']
        user.user_type = "N"
        user.save()

        return user


class User(AbstractUser):
    USER_TYPE_DJANGO = 'D'
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_NAVER = 'N'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_NAVER, 'Naver'),
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='D')
    name = models.CharField(max_length=15, blank=True, null=True) # 유저의 실제 이름
    username = models.CharField(max_length=30, unique=False)
    nickname = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    road_address = models.CharField(max_length=100, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)

    profile_image = CustomImageField(
        upload_to='user_profile_img',
        blank=True,
        default_static_image='',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    # 위에서 커스터마이징한 UserManager를 사용할 수 있게 함.
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.email

    def get_username(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email