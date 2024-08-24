from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from network.permissions import IsOwner, IsModerator, IsActiveUser
from .models import Product
from .serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    """
    API-представление для создания нового продукта.
    Позволяет аутентифицированным и активным пользователям добавлять продукты.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProductListView(generics.ListAPIView):
    """
    API-представление для получения списка всех продуктов.
    Позволяет аутентифицированным и активным пользователям просматривать список всех продуктов.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class ProductDetailView(generics.RetrieveAPIView):
    """
    API-представление для получения информации о продукте по его ID.
    Позволяет аутентифицированным и активным пользователям просматривать детали конкретного продукта.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]


class ProductUpdateView(generics.UpdateAPIView):
    """
    API-представление для обновления информации о продукте.
    Позволяет владельцу или модератору изменять информацию о продукте.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        if product.creator == user or user.groups.filter(name='moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class ProductDeleteView(generics.DestroyAPIView):
    """
    API-представление для удаления продукта.
    Позволяет владельцу или модератору удалять продукты.
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActiveUser, IsOwner | IsModerator]
