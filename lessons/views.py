from rest_framework import generics, viewsets

from users.permissions import IsModer, IsNotModer, IsOwner

from .models import Course, Lesson
from .serializers import (CourseDetailSerializer, CourseListSerializer,
                          LessonSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_context(self):
        """Передаём request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        """Фильтруем курсы: модераторы видят все, обычные - только свои"""
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            # Создавать могут только обычные пользователи
            self.permission_classes = (IsNotModer,)
        elif self.action in ["update", "partial_update"]:
            # Редактировать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "retrieve":
            # Просматривать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            # Удалять могут только владельцы (и не модераторы)
            self.permission_classes = (IsNotModer, IsOwner)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, обычные - только свои"""
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            # Создавать могут только обычные пользователи
            self.permission_classes = (IsNotModer,)
        else:
            # Просматривать список могут все авторизованные (с фильтрацией в get_queryset)
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            # Редактировать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.request.method == "DELETE":
            # Удалять могут только владельцы (и не модераторы)
            self.permission_classes = (IsNotModer, IsOwner)
        else:
            # Просматривать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Subscription
from .serializers import SubscriptionSerializer


class SubscriptionView(APIView):
    """APIView для управления подпиской на курс"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Проверка статуса подписки"""
        user = request.user
        course_id = request.query_params.get('course_id')

        if not course_id:
            return Response(
                {"error": "Не указан ID курса"},
                status=400
            )

        course = get_object_or_404(Course, id=course_id)

        is_subscribed = Subscription.objects.filter(
            user=user,
            course=course
        ).exists()

        return Response({
            "is_subscribed": is_subscribed,
            "course_id": course_id
        }, status=200)

    def post(self, request, *args, **kwargs):
        """Создание или удаление подписки"""
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Не указан ID курса"},
                status=400
            )

        # Получаем курс
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли подписка
        subscription = Subscription.objects.filter(
            user=user,
            course=course
        )

        # Если подписка есть - удаляем
        if subscription.exists():
            subscription.delete()
            return Response({
                "message": "Подписка удалена",
                "is_subscribed": False,
                "course_id": course_id
            }, status=200)

        # Если подписки нет - создаём
        else:
            try:
                new_subscription = Subscription.objects.create(
                    user=user,
                    course=course
                )
                serializer = SubscriptionSerializer(new_subscription)
                return Response({
                    "message": "Подписка добавлена",
                    "is_subscribed": True,
                    "subscription": serializer.data,
                    "course_id": course_id
                }, status=201)
            except IntegrityError:
                return Response({
                    "error": "Подписка уже существует"
                }, status=400)