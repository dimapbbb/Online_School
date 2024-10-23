from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'owner', 'title', 'description', 'link_to_video', 'course')
        validators = [UrlValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    subscribe = SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)

    get_link_for_payment = SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'price', 'description', 'lessons_count', 'lessons', 'subscribe', 'get_link_for_payment')

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_subscribe(self, obj):
        if self.context.get('request').user in [subscribe.user for subscribe in obj.subscribers.all()]:
            return True
        else:
            return False

    @staticmethod
    def get_get_link_for_payment(obj):
        return f"http://localhost:8000/payment_course/{obj.pk}/"
