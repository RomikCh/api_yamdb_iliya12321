from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_year, validate_username


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[validate_username]
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
        max_length=255,
        verbose_name='Роль',
        choices=ROLES,
        default='user'
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'


class CategoryAndGenre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор'
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(CategoryAndGenre):

    class Meta(CategoryAndGenre.Meta):
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


class Genre(CategoryAndGenre):

    class Meta(CategoryAndGenre.Meta):
        verbose_name = 'Жанры',
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год издания',
        validators=[validate_year]
    )
    description = models.TextField(
        'описание',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Название категории',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Название жанра',
        related_name='titles',
        through='GenreAndTitle',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Название произведения',
        verbose_name_plural = 'Названия произведений'


class GenreAndTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.genre}'

    class Meta:
        verbose_name = 'Жанр и название',
        verbose_name_plural = 'Жанры и названия'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
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
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField("Текст", help_text="Комментарий")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

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
