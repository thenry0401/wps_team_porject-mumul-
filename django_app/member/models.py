from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class MyUser(AbstractUser):
    username = models.CharField(max_length=30)
    profile_image = models.ImageField(upload="profile_img")
    email = models.EmailField(unique=True, blank=True)