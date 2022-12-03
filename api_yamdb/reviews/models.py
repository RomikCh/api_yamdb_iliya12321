import random

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(
        self,
        username,
        email,
        password,
        **other_fields
    ):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Для суперпользователя is_staff '
                             'должен быть равен True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Для суперпользователя is_superuser '
                             'должен быть равен True')

        if not email:
            raise ValueError('Введите email!')

        if not username:
            raise ValueError('Введите username!')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(
        self,
        username,
        email,
        **other_fields
    ):
        if not email:
            raise ValueError('Введите email!')

        if not username:
            raise ValueError('Введите username!')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **other_fields
        )
        password = random.randint(10000, 99999)**2
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
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
    confirmation_code = models.SlugField(
        max_length=5,
        null=True,
        blank=True
    )

    objects = UserManager()

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор категории',
        max_length=50
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


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

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанры',
        verbose_name_plural = 'Жанры'


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

    class Meta:
        verbose_name = 'Название',
        verbose_name_plural = 'Названия'


class GenreAndTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'жанр {self.title} - {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(
                1, message='Убедитесь, что введенное число больше или равно 1'
            ),
            MaxValueValidator(
                10, message=(
                    'Убедитесь, что введенное число меньше или равно 10'
                )
            )
        ],
    )
    text = models.TextField("Текст", help_text="Отзыв")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return '"{}" - отзыв на "{}" Автор: "{}"'.format(
            self.text,
            self.title,
            self.author
        )

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField("Текст", help_text="Комментарий")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} - комментарий на данный отзыв: {} Автор: {}'.format(
            self.text,
            self.review,
            self.author
        )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'
