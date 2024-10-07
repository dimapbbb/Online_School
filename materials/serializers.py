from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'description')


class LessonSerializer(serializers.ModelSerializer):

     class Meta:
         model = Lesson
         fields = ('id', 'title', 'description', 'link_to_video', 'course')
