from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    link = serializers.URLField(
        validators=[validate_youtube_url],
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'preview', 'description', 'link', 'course', 'owner']
        read_only_fields = ['owner']


class CourseListSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для списка курсов"""
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()  # Добавляем поле подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'owner', 'is_subscribed']
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False


class CourseDetailSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор для курса с уроками"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # Добавляем поле подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'owner', 'is_subscribed']
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['id', 'created_at']