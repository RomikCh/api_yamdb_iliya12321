from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=25,
        choices=ROLES,
        default='user'
    )


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(
                1,message='Убедитесь, что введено число больше или равно 1'
            ),
            MaxValueValidator(10, message='Убедитесь, что введено число меньше или равно 10')
        ],
    )
    text = models.TextField("Текст", help_text="Отзыв")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

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
