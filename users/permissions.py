from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="moders").exists()


class IsNotModer(permissions.BasePermission):
    message = "Модератор не может выполнять это действие"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return not request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user
