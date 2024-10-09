from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentListAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    # users
    path('update_user/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    # payments
    path('payments_list/', PaymentListAPIView.as_view(), name='payments_list'),
]