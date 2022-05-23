from django.urls import path

from accounts.api.views import (
    UserCreateAPIView,
    UserOTPVerifyAPIView,
    UserResetPasswordConfirmView,
    UserResetPasswordOTPRequestView,
)

app_name = "accounts"

urlpatterns = [
    path("create/", UserCreateAPIView.as_view(), name="create"),
    path("verify/", UserOTPVerifyAPIView.as_view(), name="otp-verify"),
    path("reset/", UserResetPasswordOTPRequestView.as_view(), name="reset-password"),
    path(
        "reset/verify/", UserResetPasswordConfirmView.as_view(), name="reset-password"
    ),
]
