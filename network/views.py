from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import NetworkEntity
from .permissions import IsOwner, IsModerator, IsActiveUser
from .serializers import NetworkEntitySerializer


class NetworkEntityCreateView(generics.CreateAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет аутентифицированным и активным пользователям создавать разделы.
    """
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class NetworkEntityListView(generics.ListAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет аутентифицированным и активным пользователям просматривать список всех участников сети.
    """
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    filterset_fields = ['country']  # Позволяет фильтровать по стране


class NetworkEntityDetailView(generics.RetrieveAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет аутентифицированным и активным пользователям просматривать детали конкретного участника сети.
    """
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class NetworkEntityUpdateView(generics.UpdateAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет владельцу или модератору редактировать информацию об участнике сети.
    """
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        network_id = self.kwargs['pk']
        network = NetworkEntity.objects.get(pk=network_id)
        if network.creator == user or user.groups.filter(name='moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class NetworkEntityDeleteView(generics.DestroyAPIView):
    """
    API-представление для создания нового участника сети.
    Позволяет владельцу или модератору удалять участников сети.
    """
    queryset = NetworkEntity.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]
