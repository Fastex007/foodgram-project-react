from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'username': {
                'required': True
            },
            'password': {
                'required': True
            },
            'email': {
                'required': True
            },
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            },
        }


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_anonymous:
                return False
            return Follow.objects.filter(user=user, author=obj.id).exists()
        return False
