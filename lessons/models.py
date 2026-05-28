from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lessons/course_previews",
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    description = models.CharField(
        max_length=200, verbose_name="Описание", help_text="Введите описание"
    )

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
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    link = models.URLField(verbose_name="Ссылка", help_text="Введите ссылку на урок")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
