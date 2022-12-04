from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from accounts.api.otp import OTP
from accounts.api_admin.serializers import (
    SMSCreditAdminSerializer,
    UserCreateAdminSerializer,
    UserListAdminSerializer,
    UserRetrieveAdminSerializer,
    UserUpdateAdminSerializer,
)
from accounts.filters import UserFilter
from common.paginations import StandardResultsSetPagination

User = get_user_model()


class UserCreateAdminAPIView(CreateAPIView):
    """Admin Create API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserCreateAdminSerializer
    queryset = User.objects.all()


class UserListAdminAPIView(ListAPIView):
    """User List API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserListAdminSerializer
    queryset = User.objects.all().order_by("-id")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]
    filterset_class = UserFilter
    pagination_class = StandardResultsSetPagination


class UserRetrieveAdminAPIView(RetrieveAPIView):
    """User Retrieve API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserRetrieveAdminSerializer
    queryset = User.objects.all()


class UserUpdateAdminAPIView(UpdateAPIView):
    """User Update API View."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserUpdateAdminSerializer
    queryset = User.objects.all()


class GetSMSCreditAdminAPIView(GenericAPIView):
    """Check credit of SMS provider."""

    serializer_class = SMSCreditAdminSerializer

    def get(self, request, *args, **kwargs):
        otp = OTP().getCredit()
        serializer = self.get_serializer(otp)
        return Response(serializer.data)
