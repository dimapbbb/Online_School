from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (UserUpdateAPIView,
                         PaymentListAPIView,
                         UserRetrieveAPIView,
                         UserCreateAPIView,
                         UserListAPIView,
                         UserDestroyAPIView,
                         SubscriptionAPIView)

app_name = UsersConfig.name

urlpatterns = [
    # token
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # users
    path('create_user/', UserCreateAPIView.as_view(), name='create_user'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('update_user/<int:pk>/', UserUpdateAPIView.as_view(), name='update_user'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('delete_user/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
    # payments
    path('payments_list/', PaymentListAPIView.as_view(), name='payments_list'),
    # subscription
    path('subscribe/<int:pk>', SubscriptionAPIView.as_view(), name='subscription'),
]