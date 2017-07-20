from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

# Create your models here.
from utils.fields.custom_imagefield import CustomImageField


class UserManager(DefaultUserManager):

    def get_or_create_facebook_user(self, user_pk):
        user = User.objects.get(pk=user_pk)
        user.user_type = user.USER_TYPE_FACEBOOK
        user.save()
        return user

class User(AbstractUser):
    USER_TYPE_DJANGO = 'D'
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='D')
    nickname = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    profile_image = CustomImageField(
        upload_to='user_profile_img',
        blank=True,
        default_static_image='',
    )

    # 위에서 커스터마이징한 UserManager를 사용할 수 있게 함.
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username

