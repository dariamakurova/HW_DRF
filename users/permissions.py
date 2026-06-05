from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsNotModer(permissions.BasePermission):
    message = "Модератор не может выполнять это действие"

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
