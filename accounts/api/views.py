from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.api.serializers import (
    UserCreateOTPVerifySerializer,
    UserCreateSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordOTPRequestSerializer,
    UserResetPasswordOTPVerifySerializer,
)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """User Create Post API View."""

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserCreateOTPVerifyAPIView(generics.UpdateAPIView):
    """User Create OTP Verify Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserCreateOTPVerifySerializer
    queryset = User.objects.all()

    def get_object(self):
        """Get the object using the request data.

        {
            ...
            "username": "username",
            ...
        }

        Returns
            ok: User object
            error: 404 error

        """
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)


class UserResetPasswordOTPRequestAPIView(generics.UpdateAPIView):
    """User Reset Password OTP Request Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordOTPRequestSerializer
    queryset = User.objects.all()

    def get_object(self):
        """Get the object using the request data.

        {
            ...
            "username": "username",
            ...
        }

        Returns
            ok: User object
            error: 404 error

        """
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)


class UserResetPasswordOTPVerifyAPIView(generics.UpdateAPIView):
    """User Reset Password OTP Verify Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordOTPVerifySerializer
    queryset = User.objects.all()

    def get_object(self):
        """Get the object using the request data.

        {
            ...
            "username": "username",
            ...
        }

        Returns
            ok: User object
            error: 404 error

        """
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)


class UserResetPasswordConfirmAPIView(generics.UpdateAPIView):
    """User Reset Password Confirm Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordConfirmSerializer
    queryset = User.objects.all()

    def get_object(self):
        """Get the object using the request data.

        {
            ...
            "username": "username",
            ...
        }

        Returns
            ok: User object
            error: 404 error

        """
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)
