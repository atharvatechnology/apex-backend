from django.urls import path

from accounts.api.views import (
    UserCreateAPIView,
    UserCreateOTPVerifyAPIView,
    UserResetPasswordConfirmAPIView,
    UserResetPasswordOTPRequestAPIView,
    UserResetPasswordOTPVerifyAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("create/", UserCreateAPIView.as_view(), name="create"),
    path("create/verify/", UserCreateOTPVerifyAPIView.as_view(), name="otp-verify"),
    path("reset/", UserResetPasswordOTPRequestAPIView.as_view(), name="reset-password"),
    path(
        "reset/verify/",
        UserResetPasswordOTPVerifyAPIView.as_view(),
        name="reset-password-verify",
    ),
    path(
        "reset/confirm/",
        UserResetPasswordConfirmAPIView.as_view(),
        name="reset-password-confirm",
    ),
]
