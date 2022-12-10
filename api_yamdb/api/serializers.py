import datetime

from rest_framework import serializers

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
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate(self, data):
        username = data['username']
        email = data['email']

        if not User.objects.filter(
            username=username,
            email=email
        ).exists():
            if User.objects.filter(
                username=username,
            ).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким никнеймом уже существует!'
                )

            if User.objects.filter(
                email=email
            ).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким адресом уже существует!'
                )

            if username == 'me':
                raise serializers.ValidationError(
                    'Использовать me в качестве ника запрещено!'
                )
        return data


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год издания не может быть больше текущего года'
            )
        return value

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
