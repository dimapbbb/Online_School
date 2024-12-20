from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from custom.mixins import GetOwnerMixin
from materials.models import Course, Lesson
from materials.paginators import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_mail_of_update
from users.permissions import IsModerator, IsOwner


class CourseViewSet(GetOwnerMixin, viewsets.ModelViewSet):
    """ CRUD для курсов """
    pagination_class = MyPagination
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get(self, request):
        paginated_queryset = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        update_course = serializer.save()
        dt_now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())

        if update_course.last_update < dt_now - timedelta(hours=4):
            send_mail_of_update.delay(update_course.pk)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = []
        elif self.action == 'update':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'partial_update':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]

        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    pagination_class = MyPagination
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = []

    def get(self, request):
        paginated_queryset = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(GetOwnerMixin, generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(GetOwnerMixin, generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(GetOwnerMixin, generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
