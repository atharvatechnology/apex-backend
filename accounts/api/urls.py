from django.urls import path

from accounts.api.views import (
    UserCreateAPIView,
    UserCreateOTPVerifyAPIView,
    UserResetPasswordConfirmAPIView,
    UserResetPasswordOTPRequestAPIView,
    UserResetPasswordOTPVerifyAPIView,
)
from accounts.api_admin.views import (
    UserCreateAdminAPIView,
    UserListAdminAPIView,
    UserRetrieveAdminAPIView,
    UserUpdateAdminAPIView,
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

urlpatterns += [
    path("admin/create/", UserCreateAdminAPIView.as_view(), name="admin-create"),
    path("admin/list/", UserListAdminAPIView.as_view(), name="admin-list"),
    path(
        "admin/retrieve/<int:pk>/",
        UserRetrieveAdminAPIView.as_view(),
        name="admin-retrieve",
    ),
    path(
        "admin/update/<int:pk>/", UserUpdateAdminAPIView.as_view(), name="admin-update"
    ),
]
