from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from accounts.api_admin.serializers import (
    UserCreateAdminSerializer,
    UserListAdminSerializer,
    UserRetrieveAdminSerializer,
    UserUpdateAdminSerializer,
)

from ..filters import UserFilter

User = get_user_model()


class UserCreateAdminAPIView(generics.CreateAPIView):
    """Admin Create API View."""

    permission_classes = [AllowAny, IsAdminUser]
    serializer_class = UserCreateAdminSerializer
    queryset = User.objects.all()


class UserListAdminAPIView(generics.ListAPIView):
    """User List API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserListAdminSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    filterset_class = UserFilter


class UserRetrieveAdminAPIView(generics.RetrieveAPIView):
    """User Retrieve API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserRetrieveAdminSerializer
    queryset = User.objects.all()


class UserUpdateAdminAPIView(generics.UpdateAPIView):
    """User Update API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserUpdateAdminSerializer
    queryset = User.objects.all()
