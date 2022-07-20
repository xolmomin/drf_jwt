from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError, Serializer
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings

class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # d = {
        #     'username ': self.user.username,
        # }
        data['data'] = UserDataSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class UserModelSerializer(ModelSerializer):
    first_name = CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')


class RegisterModelSerializer(Serializer):
    username = CharField(max_length=255)
    password = CharField(max_length=255)

    def validate_username(self, username):
        if not username.isalpha():
            raise ValidationError('Faqat harflar bilan')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Bu username borku')

        return username

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user

    # confirm_password = CharField(max_length=255)

    # def create(self, validated_data):
    #     print(validated_data)
    #     username = validated_data['username']
    #     if User.objects.filter(username=username).exists():
    #         print(123)
    #         raise ValidationError('Bu username borku')
    #
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super().create(validated_data)

    class Meta:
        model = User
        fields = ('username', 'password')
