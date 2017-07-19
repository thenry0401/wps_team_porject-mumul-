from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.fields.custom_imagefield import CustomImageField

class UserManager(BaseUserManager):
    pass


class MyUser(AbstractUser):
    USER_TYPE_DJANGO = 'D'
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    nickname = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    profile_image = CustomImageField(
        upload_to='user_profile_img',
        blank=True,
        default_static_image='',
    )

    def __str__(self):
        return self.nickname or self.username