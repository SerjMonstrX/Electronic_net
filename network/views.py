from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from .models import NetworkEntity
from .permissions import IsOwner, IsModerator, IsActiveUser
from .serializers import NetworkEntitySerializer


class NetworkEntityCreateView(generics.CreateAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет аутентифицированным пользователям создавать разделы.
    """
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class NetworkEntityListView(generics.ListAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    filterset_fields = ['country']  # Позволяет фильтровать по стране


class NetworkEntityDetailView(generics.RetrieveAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class NetworkEntityUpdateView(generics.UpdateAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]


class NetworkEntityDeleteView(generics.DestroyAPIView):
    queryset = NetworkEntity.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]
