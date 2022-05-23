from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.api.serializers import (
    UserCreateSerializer,
    UserOTPVerifySerializer,
    UserResetPasswordRequestSerializer,
    UserResetPasswordVerifySerializer,
)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserOTPVerifyAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserOTPVerifySerializer
    queryset = User.objects.all()

    def get_object(self):
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)


class UserResetPasswordOTPRequestView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordRequestSerializer
    queryset = User.objects.all()

    def get_object(self):
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)


class UserResetPasswordConfirmView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordVerifySerializer
    queryset = User.objects.all()

    def get_object(self):
        username = self.request.data.get("username", None)
        return get_object_or_404(self.queryset, username=username)
