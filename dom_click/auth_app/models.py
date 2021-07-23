from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(blank=False, unique=True, verbose_name='email')


class Client(models.Model):
    """Модель клиента и работника"""
    first_name = models.CharField(
        max_length=128, blank=False, verbose_name='имя')
    last_name = models.CharField(
        max_length=128, blank=False, verbose_name='фамилия')
    phone_regex = RegexValidator(regex=r'^\+7\d{10}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=12,
                                    blank=True, verbose_name='номер телефона')
    email = models.EmailField(blank=True, verbose_name='email')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='актив')
    is_worker = models.BooleanField(
        default=False, db_index=True, verbose_name='сотрудник')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    edited = models.DateTimeField(auto_now=True, verbose_name='изменен')

    def __str__(self):
        if self.is_worker:
            return f'{self.first_name} {self.last_name} - СОТРУДНИК'
        return f'{self.first_name} {self.last_name}'
