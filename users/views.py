# users/views.py
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Фильтрация
    filterset_fields = {
        'payment_method': ['exact'],  # точное совпадение по способу оплаты
        'course': ['exact', 'isnull'],  # фильтр по конкретному курсу или отсутствию курса
        'lesson': ['exact', 'isnull'],  # фильтр по конкретному уроку или отсутствию урока
    }

    # Сортировка
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # по умолчанию сортировка от новых к старым