from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CourseViewSet, LessonListCreateView,
                    LessonRetrieveUpdateDestroyView)

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
]
