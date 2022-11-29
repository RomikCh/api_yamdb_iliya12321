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


class Category(models.Model):
    name = models.CharField(
        verbose_name='категория',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор категории',
        max_length=50
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='жанр',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор жанра',
        max_length=50,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='год издания'
    )
    description = models.TextField(
        'описание',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        through='GenreAndTitle',
    )

    def __str__(self):
        return self.name


class GenreAndTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'жанр {self.title} - {self.genre}'
