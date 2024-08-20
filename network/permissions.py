from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь создателем объекта.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsActiveUser(BasePermission):
    """
    Разрешает доступ только активным пользователям.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
