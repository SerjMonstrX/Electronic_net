from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import NetworkEntity
from .serializers import NetworkEntitySerializer


class NetworkEntityCreateView(generics.CreateAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer


class NetworkEntityDetailView(generics.RetrieveAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer


class NetworkEntityUpdateView(generics.UpdateAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer


class NetworkEntityDeleteView(generics.DestroyAPIView):
    queryset = NetworkEntity.objects.all()


class NetworkEntityListView(generics.ListAPIView):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']  # Позволяет фильтровать по стране
