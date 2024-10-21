from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from custom.mixins import GetOwnerMixin
from materials.models import Course, Lesson
from materials.paginators import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(GetOwnerMixin, viewsets.ModelViewSet):
    pagination_class = MyPagination
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get(self, request):
        paginated_queryset = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
