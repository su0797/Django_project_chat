from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.
'''
Auth User model
- 생성
- 삭제
- 수정
--> UserManager helper class 도움주는 클래스
'''


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        # now = timezone.now() # 현재시간 -> UTC
        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = True,
            last_login = now, 
            date_joined = now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    # create_superuser
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
