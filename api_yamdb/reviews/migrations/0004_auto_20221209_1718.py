# Generated by Django 2.2.16 on 2022-12-09 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_genreandtitle_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Убедитесь, что введенное число больше или равно 1'), django.core.validators.MaxValueValidator(10, message='Убедитесь, что введенное число меньше или равно 10')], verbose_name='Оценка'),
        ),
    ]