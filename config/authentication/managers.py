# shop_drf > authentication > managers.py
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    # All user
    def create_user(self, username, password=None, **extra_fields):
    
        if username is None:
            raise TypeError('Users must have a username.')

        if password is None:
            raise TypeError('Users must have a password.')
    
        user = self.model(
            username = self.normalize_email(username),
            # 중복 최소화를 위한 정규화
            **extra_fields
        )
        
        user.is_superuser = False

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()
        
        return user

    # admin user
    def create_superuser(self, username, password, **extra_fields):
        print('xxxx')
        if password is None:
            raise TypeError('Superuser must have a password.')
        
        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(username, password, **extra_fields)
        # 관리자로 지정
        user.is_superuser = True
        user.is_staff = True
        user.name = "admin"
        user.dateOfBirth = "1900-01-01"
        user.save()
        
        return user