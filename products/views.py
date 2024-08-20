from rest_framework import generics, permissions
from network.permissions import IsOwner, IsModerator, IsActiveUser
from .models import Product
from .serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    """
    API-представление для создания нового продукта.
    Позволяет аутентифицированным пользователям добавлять продукты.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class ProductListView(generics.ListAPIView):
    """
    API-представление для получения списка всех продуктов с возможностью фильтрации по стране.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class ProductDetailView(generics.RetrieveAPIView):
    """
    API-представление для получения информации о продукте по его ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class ProductUpdateView(generics.UpdateAPIView):
    """
    API-представление для обновления информации о продукте.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]


class ProductDeleteView(generics.DestroyAPIView):
    """
    API-представление для удаления продукта.
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]

