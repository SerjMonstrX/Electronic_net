from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer
from users.models import User


class UsersListAPIView(generics.ListAPIView):
    """
    Представление для получения списка пользователей.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания нового пользователя.
    """
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Представление для получения информации о конкретном пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    """
    Представление для обновления информации о пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    """
    Представление для удаления пользователя.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
