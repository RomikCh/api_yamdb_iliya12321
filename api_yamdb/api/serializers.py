from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import validate_username, validate_year
from reviews.models import Category, Comment, Genre, Review, Title, User


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
    username = serializers.CharField(
        max_length=150,
        required=True,
        # validators=['кастомная хрень']
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


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
        allow_null=True,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        request = self.context['request']
        author = request.user
        title = get_object_or_404(Title, id=title_id)
        if (
            title.reviews.filter(author=author).exists() 
            and request.method != 'PATCH'
        ):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data


class CategoryGenre(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        model = Category


class GenreSerializer(CategoryGenre):

    class Meta(CategoryGenre.Meta):
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
