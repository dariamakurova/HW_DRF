from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    user_email = serializers.ReadOnlyField(source="user.email")
    course_name = serializers.ReadOnlyField(source="course.name", read_only=True)
    lesson_name = serializers.ReadOnlyField(source="lesson.name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "payment_date",
            "course",
            "course_name",
            "lesson",
            "lesson_name",
            "amount",
            "payment_method",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
