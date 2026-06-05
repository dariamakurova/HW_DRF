from rest_framework import permissions

class IsModer(permissions.BasePermission):
    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="moders").exists()

class IsNotModer(permissions.BasePermission):
    message = 'Модератор не может выполнять это действие'

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter(name="moders").exists()