from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count')

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):

     class Meta:
         model = Lesson
         fields = ('id', 'title', 'description', 'link_to_video', 'course')
