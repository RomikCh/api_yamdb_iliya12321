from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    rating = models.IntegerField(
        null=True,
        verbose_name='Рейтинг произведения',
        default=None
    )

    def __str__(self):
        return self.name


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


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField("Текст", help_text="Комментарий")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    def __str__(self):
        return '"{}" - комментарий на данный отзыв: "{}" Автор: "{}"'.format(
            self.text,
            self.review,
            self.author
        )

    class Meta:
        ordering = ["-pub_date"]
