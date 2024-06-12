from django.urls import path

from accounts.api.views import (
    StudentQRView,
    UserCreateAPIView,
    UserCreateOTPVerifyAPIView,
    UserDeletionAPIView,
    UserDetailAPIView,
    UserResetPasswordConfirmAPIView,
    UserResetPasswordOTPRequestAPIView,
    UserResetPasswordOTPVerifyAPIView,
    UserUpdateAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("create/", UserCreateAPIView.as_view(), name="create"),
    path("me/", UserDetailAPIView.as_view(), name="retrive"),
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
    path("update/me/", UserUpdateAPIView.as_view(), name="update"),
    path("qr/", StudentQRView.as_view(), name="qrretrive"),
    path("delete/request/", UserDeletionAPIView.as_view(), name="delete_request"),
]
