from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from accounts.api_admin.serializers import UserListSerializer

# from accounts.models import Profile

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    """User List API View."""

    permission_classes = [AllowAny]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username", "phone_number"]
