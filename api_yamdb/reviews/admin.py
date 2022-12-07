from django.contrib import admin

from .models import (
    User, Review, Comment, Genre, Title, Category, GenreAndTitle
)


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(GenreAndTitle)
