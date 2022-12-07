from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    User, Review, Comment, Genre, Title, Category, GenreAndTitle
)

class UserResource(resources.ModelResource):
    
    class Meta: 
        model = User
        fields = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


class CategoryResource(resources.ModelResource):
    
    class Meta: 
        model = Category
        fields = (
        'id',
        'name',
        'slug',
    )


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = (
        'id',
        'name',
        'slug',
    )


class GenreResource(resources.ModelResource):
    
    class Meta: 
        model = Genre
        fields = (
        'id',
        'name',
        'slug',
    )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = (
        'id',
        'name',
        'slug',
    )


class TitleResource(resources.ModelResource):
    
    class Meta: 
        model = Title
        fields = (
        'id',
        'name',
        'year',
        'description'
    )


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = (
        'id',
        'name',
        'year',
        'description'
    )


class ReviewResource(resources.ModelResource):
    
    class Meta: 
        model = Review
        fields = (
        'id',
        'text',
        'pub_date',
        'author_id'
        'title_id'
        'score'
    )


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    list_display = (
        'id',
        'text',
        'pub_date',
        'score'
    )


class CommentResource(resources.ModelResource):
    
    class Meta: 
        model = Comment
        fields = (
        'id',
        'text',
        'pub_date',
        'author_id'
        'review_id'
    )


class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    list_display = (
        'id',
        'text',
        'pub_date',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GenreAndTitle)
