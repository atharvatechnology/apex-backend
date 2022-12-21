from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.api.serializers import (
    StudentQRSerializer,
    UserCreateOTPVerifySerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordOTPRequestSerializer,
    UserResetPasswordOTPVerifySerializer,
    UserUpdateSerializer,
)
from accounts.filters import StudentFilter
from accounts.models import Profile, Role
from common.api.views import BaseReportGeneratorAPIView

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """User Create Post API View."""

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.roles.add(Role.STUDENT)


class UserCreateOTPVerifyAPIView(UpdateModelMixin, LoginView):
    """User Create OTP Verify Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserCreateOTPVerifySerializer
    queryset = User.objects.all()

    user = None
    access_token = None
    token = None

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        self.serializer = serializer

        self.login()
        return self.get_response()


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


class UserResetPasswordConfirmAPIView(UpdateModelMixin, LoginView):
    """User Reset Password Confirm Patch API View."""

    permission_classes = [AllowAny]
    http_method_names = ["patch"]
    serializer_class = UserResetPasswordConfirmSerializer
    queryset = User.objects.all()

    user = None
    access_token = None
    token = None

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        self.serializer = serializer

        self.login()
        return self.get_response()


class UserUpdateAPIView(generics.UpdateAPIView):
    """User Detail Update API View."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserDetailAPIView(generics.RetrieveAPIView):
    """User Detail API View."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class StudentQRView(generics.RetrieveAPIView):
    """Student QR API View."""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentQRSerializer
    # queryset = Profile.objects.all()

    def get_object(self):
        return self.request.user.profile


class StudentReportGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    queryset = Profile.objects.all()
    filterset_class = StudentFilter
    model_name = "StudentProfile"

    # {
    # "model_fields":["username","fullname","email","college_name","faculty"]
    # }
