import random

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Comment,
    User,
    Review, 
    Category,
    Genre,
    Title
)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        source='password',
        read_only=True,
        required=False
    )
    is_active = serializers.HiddenField(
        read_only=True,
        default=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'confirmation_code',
            'is_active'
        )
        lookup_field = 'username'


class SignUpSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        source='password',
        default=random.randint(10000, 99999),
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'confirmation_code'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать me как username!'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return Review.objects.aggregate(Avg('score'))


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
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
