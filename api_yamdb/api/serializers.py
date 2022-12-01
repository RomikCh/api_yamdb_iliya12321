from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, User, Review, Category, Genre, Title


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставили отзыв!',
            )
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_filed = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_filed = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'
