from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course
from materials.services import create_session, session_retrieve
from users.models import User, Payment, Subscriptions
from users.permissions import IsOwnerAccount, IsSuperUser
from users.serializers import UserSerializer, PaymentSerializer, UserDetailSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    swagger_schema = None


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerAccount]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == super().get_object():
            return UserDetailSerializer
        return UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerAccount]
    swagger_schema = None


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsSuperUser]
    swagger_schema = None

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['method', 'paid_course', 'paid_lesson']


class SubscriptionAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course = Course.objects.get(id=self.kwargs.get('pk'))

        for subscription in user.subscriptions.all():
            if subscription.course == course:
                subscription.delete()
                message = "Подписка удалена"
                return Response({'message': message})

        Subscriptions.objects.create(user=user, course=course)
        message = "Подписка добавлена"

        return Response({'message': message})


class PaymentCourseAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs.get('pk'))
        session = create_session(course)

        Payment.objects.create(
            user = self.request.user,
            paid_course = course,
            amount = course.price,
            method = 'transfer',
            session_id = session.get('id'),
            status = session.get('status')
        )
        return Response({'link_for_payment': session.get('url')})


class GetStatusPaymentAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment = Payment.objects.get(
            user=self.request.user,
            paid_course_id = self.kwargs.get('pk')
        )
        status = session_retrieve(payment.session_id).get('status')
        payment.status = status
        payment.save()

        return Response({'Статус платежа': status})



