from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson_create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lessons_list/', LessonListAPIView.as_view(), name='lessons'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('update_lesson/<int:pk>', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('delete_lesson/<int:pk>', LessonDestroyAPIView.as_view(), name='delete_lesson')
] + router.urls
