from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'link_to_video', 'course')
        validators = [UrlValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    subscribe = SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons', 'subscribe')

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_subscribe(self, obj):
        if self.context.get('request').user in [subscribe.user for subscribe in obj.subscribers.all()]:
            return True
        else:
            return False
