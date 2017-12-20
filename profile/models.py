# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# from shop.models import Order

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=u'username', max_length=250, blank=True)
    first_name = models.CharField(verbose_name='Имя',  max_length=255, default="")
    last_name = models.CharField(verbose_name='Фамилия',  max_length=255, blank=True, null=True, default="")
    mobiphone = models.CharField(verbose_name='Мобильный Телефон',  max_length=255, blank=True, null=True, default="")

    phone = models.CharField(verbose_name=u'Телефон', max_length=250, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    address = models.TextField(verbose_name=u'Адресс доставки', default="", blank=True, null=True)

    date_of_birth = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    whishlist = JSONField(verbose_name='whishlist', blank=True, null=True)
    removed = JSONField(verbose_name='removed', blank=True, null=True)
    removedwithdetails = JSONField(verbose_name='removed with details', blank=True, null=True)
    viewed = JSONField(verbose_name='Просмотренные', blank=True, null=True)
    emails = JSONField(verbose_name='Emails', blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
