from django.db import models

# Create your models here.
from builtins import property, ValueError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, name, nickname, email, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, nickname, email, password):
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            name = name,
        )

        user.is_superuser= True

        if user.is_superuser is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, verbose_name='이름')
    nickname= models.CharField(max_length=10, unique=True, verbose_name='닉네임')
    email = models.EmailField(max_length=255, unique=True, verbose_name='이메일')
    reside = models.CharField(max_length=50, verbose_name='거주지', blank=True)    # 나중에 위젯이랑 연결
    date_joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nickname',]

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.name + "(nickname:{})".format(self.nickname)
    def get_full_name(self):
        return self.nickname
    def get_short_name(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_superuser

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
