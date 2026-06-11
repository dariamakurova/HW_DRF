from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lessons/course_previews",
        null=True,
        blank=True,
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    description = models.CharField(
        max_length=200, verbose_name="Описание", help_text="Введите описание"
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится урок",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="lessons/lesson_previews",
        null=True,
        blank=True,
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    link = models.URLField(verbose_name="Ссылка", help_text="Введите ссылку на урок")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки на обновления курса"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]  # Чтобы не было дублей

    def __str__(self):
        return f"{self.user.email} -> {self.course.name}"
