from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""
    user_email = serializers.ReadOnlyField(source='user.email')
    course_name = serializers.ReadOnlyField(source='course.name', read_only=True)
    lesson_name = serializers.ReadOnlyField(source='lesson.name', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'course', 'course_name',
                  'lesson', 'lesson_name', 'amount', 'payment_method']