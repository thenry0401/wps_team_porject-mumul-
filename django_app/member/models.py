from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.db import models

# Create your models here.
from requests import request, HTTPError

from utils.fields.custom_imagefield import CustomImageField


class UserManager(DefaultUserManager):

    # 페이스북으로 가입하면 user_type을 F(Facebook)으로 지정한다.
    def get_or_create_facebook_user(self, user_pk, extra_data, profile_url):
        print(extra_data)
        user = User.objects.get(pk=user_pk)
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

    # 네이버로 가입하면 user_type을 N(Naver)으로 지정한다. 그외에 커스텀 저장을 한다.
    def get_or_create_naver_user(self, user_pk, extra_data):
        print(extra_data)
        user = User.objects.get(pk=user_pk)
        user.username = extra_data['name']
        user.nickname = extra_data['nickname']
        user.email = extra_data['email']
        user.first_name = extra_data['name'][0]
        user.last_name = extra_data['name'][1:]
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
    nickname = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    jibun_address = models.CharField(max_length=100, blank=True, null=True)
    road_address = models.CharField(max_length=100, blank=True, null=True)
    profile_image = CustomImageField(
        upload_to='user_profile_img',
        blank=True,
        default_static_image='',
    )

    # 위에서 커스터마이징한 UserManager를 사용할 수 있게 함.
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username

