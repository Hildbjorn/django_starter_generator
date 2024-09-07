from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class Ranks(models.Model):
    id = models.AutoField(unique=True,
                          primary_key=True,
                          verbose_name='Код ранга')

    rank = models.CharField(max_length=255,
                            verbose_name='Ранг',
                            null=False,
                            blank=False)

    def __str__(self):
        rank = str(self.rank)

        return rank

    class Meta:
        verbose_name = 'Ранг'
        verbose_name_plural = 'Ранги'
        ordering = ['id']


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('E-mail'), unique=True)

    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя',
                                  null=True,
                                  blank=True)

    middle_name = models.CharField(max_length=100,
                                   verbose_name='Отчество',
                                   null=True,
                                   blank=True)

    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 null=True,
                                 blank=True)

    company = models.CharField(max_length=255,
                               verbose_name='Компания',
                               null=True,
                               blank=True)

    position = models.CharField(max_length=255,
                                verbose_name='Должность',
                                null=True,
                                blank=True)

    phone = models.CharField(max_length=20,
                             unique=False,
                             null=True,
                             blank=True,
                             verbose_name='Телефон',
                             db_index=True)

    rank = models.ForeignKey('Ranks',
                             on_delete=models.PROTECT,
                             null=True,
                             blank=True,
                             related_name='rank_set',
                             verbose_name='Ранг')

    agreement = models.BooleanField(unique=False,
                                    primary_key=False,
                                    default=True,
                                    verbose_name='Согласие на обработку персональных данных')

    is_staff = models.BooleanField(default=False,
                                   verbose_name='В команде')

    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный')

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if not self.first_name or not self.last_name:
            fio = str(self.email)
        elif not self.middle_name:
            fio = str(self.last_name) + " " + str(self.first_name)
        else:
            fio = str(self.last_name) + " " + str(self.first_name) + " " + str(self.middle_name)
        return fio

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name', 'middle_name']
