from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

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

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


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

    def perform_update(self, serializer):
        user = self.request.user
        newtwork_id = self.kwargs['pk']
        newtwork = NetworkEntity.objects.get(pk=newtwork_id)
        if newtwork.creator == user or user.groups.filter(name='moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class NetworkEntityDeleteView(generics.DestroyAPIView):
    queryset = NetworkEntity.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]
