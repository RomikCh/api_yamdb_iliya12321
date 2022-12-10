import random

from rest_framework import serializers

from api.validators import validate_username, validate_year
from reviews.models import (
    Comment,
    User,
    Review,
    Category,
    Genre,
    Title,
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
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        default=random.randint(10000, 99999),
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
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class CategoryAndGenre(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(CategoryAndGenre):

    class Meta(CategoryAndGenre.Meta):
        model = Category


class GenreSerializer(CategoryAndGenre):

    class Meta(CategoryAndGenre.Meta):
        model = Genre


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'name', 'year', 'description', 'category', 'genre', 'id'
        )
