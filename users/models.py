from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from stores.models import Store
from .custom_managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractBaseUser):
    BOSS = 1
    SELLER = 2
    ROLE_CHOICES = (
        (BOSS,'BOSS'),
        (SELLER,'SELLER')
    )
    username = None
    login = models.CharField(unique=True,null=True,blank=True)
    role = models.PositiveIntegerField(choices=ROLE_CHOICES,null=True)
    name = models.CharField(max_length=255,blank=True,default='')
    image = models.ImageField(upload_to='users/',null=True,blank=True)
    stores = models.ManyToManyField(Store)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "login"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.login} - {self.name}"
