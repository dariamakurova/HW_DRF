# lessons/serializers.py
from rest_framework import serializers

from .models import Course, Lesson
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    link = serializers.URLField(
        validators=[validate_youtube_url],  # Используем функцию
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'preview', 'description', 'link', 'course', 'owner']
        read_only_fields = ['owner']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор для курса с уроками"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Все уроки курса

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()


class CourseListSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для списка курсов (без уроков)"""

    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons_count"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
