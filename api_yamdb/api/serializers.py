import random

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, User, Review


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
