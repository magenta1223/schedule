from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser 
from django.utils import timezone
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(verbose_name = '이메일', unique=True)    
    objects = UserManager()    
    name = models.CharField(max_length= 20,  blank= True, null = True)
    # dateOfBirth = models.DateTimeField( blank= True, null = True)
    contact = models.CharField(max_length=10, blank= True, null = True)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default= True)

    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
        return True