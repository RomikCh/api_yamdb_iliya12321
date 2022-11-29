from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=250,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=25,
        choices=ROLES,
        default='user'
    )
