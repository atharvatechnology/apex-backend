from dj_rest_auth.jwt_auth import (
    CookieTokenRefreshSerializer,
    set_jwt_access_cookie,
    set_jwt_refresh_cookie,
)
from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.serializers import (
    StudentQRSerializer,
    UserCreateOTPVerifySerializer,
    UserCreateSerializer,
    UserDeletionSerializer,
    UserDetailSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordOTPRequestSerializer,
    UserResetPasswordOTPVerifySerializer,
    UserUpdateSerializer,
)
from accounts.models import AccountDeleteion, Role

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """User Create Post API View."""

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.roles.add(Role.STUDENT)
        group, created = Group.objects.get_or_create(name="Student")
        obj.groups.add(group)


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


class CustomLoginView(LoginView):
    def login(self):
        super().login()
        if getattr(settings, "REST_USE_JWT", False):
            cache.set(
                f"{self.user.id}-token",
                {
                    "access": str(self.access_token),
                    "refresh": str(self.refresh_token),
                },
                timeout=jwt_settings.ACCESS_TOKEN_LIFETIME.total_seconds(),
            )
            # a = cache.get(f"{self.user.id}-token")


class CustomLogoutView(LogoutView):
    def logout(self, request):
        user = self.request.user
        response = super().logout(request)
        if getattr(settings, "REST_USE_JWT", False):
            cache.delete(f"{user.id}-token")
        return response


def get_refresh_view():
    """Return a Token Refresh CBV without a circular import."""

    class RefreshViewWithCookieSupport(TokenRefreshView):
        serializer_class = CookieTokenRefreshSerializer

        def finalize_response(self, request, response, *args, **kwargs):
            if response.status_code == 200 and "access" in response.data:
                set_jwt_access_cookie(response, response.data["access"])
                response.data["access_token_expiration"] = (
                    timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
                )
            if response.status_code == 200 and "refresh" in response.data:
                set_jwt_refresh_cookie(response, response.data["refresh"])
            if response.status_code == 200 and hasattr(request, "past_user"):
                cache.set(
                    f"{request.past_user.id}-token",
                    response.data,
                    timeout=jwt_settings.ACCESS_TOKEN_LIFETIME.seconds,
                )
            return super().finalize_response(request, response, *args, **kwargs)

    return RefreshViewWithCookieSupport


class UserDeletionAPIView(generics.CreateAPIView):
    serializer_class = UserDeletionSerializer
    model = AccountDeleteion
    permission_classes = [AllowAny]

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        user = instance.user
        user.is_active = False
        user.save()
