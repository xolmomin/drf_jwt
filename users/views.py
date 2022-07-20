from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers.users import UserModelSerializer, RegisterModelSerializer, LoginSerializer


class UserList(ListAPIView, DestroyAPIView):
    pass


class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = (AllowAny,)
    # throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        """User yaratish uchun api"""
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Userlarni olish"""
        return super().list(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='register', serializer_class=RegisterModelSerializer)
    def user_register(self, request, pk=None):
        serialized_data = RegisterModelSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        data = {'message': 'User successfully created !'}
        return Response(data, status.HTTP_201_CREATED)
