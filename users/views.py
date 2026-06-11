from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Payment, User
from .permissions import IsModer, IsOwner
from .serializers import (PaymentSerializer, UserDetailSerializer,
                          UserSerializer)


class PaymentListView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = {
        "payment_method": ["exact"],
        "course": ["exact", "isnull"],
        "lesson": ["exact", "isnull"],
    }

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsOwner)
        elif self.action == "retrieve":
            self.permission_classes = (IsModer | IsOwner,)
        else:
            self.permission_classes = (IsModer,)
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """Переопределяем retrieve для проверки прав"""
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)

        user = request.user

        # Модератор может просматривать всех
        if user.groups.filter(name="moders").exists():
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        # Обычный пользователь - только себя
        if instance == user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(
            {"detail": "У вас нет прав для просмотра этого профиля"}, status=403
        )

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])
