from rest_framework import serializers

from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
