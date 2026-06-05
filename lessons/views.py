# lessons/views.py

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModer, IsNotModer, IsOwner
from .models import Course, Lesson
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

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
        if self.action == 'create':
            # Создавать могут только обычные пользователи
            self.permission_classes = (IsNotModer,)
        elif self.action in ['update', 'partial_update']:
            # Редактировать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'retrieve':
            # Просматривать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
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
        if self.request.method == 'POST':
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
        if self.request.method in ['PUT', 'PATCH']:
            # Редактировать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        elif self.request.method == 'DELETE':
            # Удалять могут только владельцы (и не модераторы)
            self.permission_classes = (IsNotModer, IsOwner)
        else:
            # Просматривать могут: модераторы ИЛИ владельцы
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()