from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.otp import OTP
from accounts.api_admin.filters import (
    FacultyAdminFilter,
    StudentAdminFilter,
    UserAdminFilter,
)
from accounts.api_admin.serializers import (
    SMSCreditAdminSerializer,
    UserCreateAdminSerializer,
    UserListAdminSerializer,
    UserMiniAdminSerializer,
    UserRetrieveAdminSerializer,
    UserStudentCreateAdminSerializer,
    UserTeacherCreateAdminSerializer,
    UserUpdateAdminSerializer,
)
from accounts.models import Role
from common.paginations import StandardResultsSetPagination
from common.permissions import IsAccountant, IsAdminOrSuperAdminOrDirector, IsCashier
from common.utils import tuple_to_list, tuple_to_list_first_elements
from courses.models import CourseCategory

User = get_user_model()


class UserRolesView(APIView):
    """Roles List API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]

    def get(self, request):
        return Response(tuple_to_list(Role.role_choices))


class UserCreateAdminAPIView(CreateAPIView):
    """Admin Create API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = UserCreateAdminSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        # Get user role.
        user_role = serializer.data["roles"]
        #  Get user role index from tuple
        role_dict = Role().role_dict()
        for roles in user_role:
            role_name = role_dict[roles]
            # Get user group
            group, created = Group.objects.get_or_create(name=role_name)
            obj.groups.add(group)


class UserStudentCreateAdminAPIView(CreateAPIView):
    """Admin Create API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsAccountant | IsCashier]
    serializer_class = UserStudentCreateAdminSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.roles.add(Role.STUDENT)
        group, created = Group.objects.get_or_create(name="Student")
        obj.groups.add(group)


class UserTeacherCreateAdminAPIView(CreateAPIView):
    """Admin Create API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = UserTeacherCreateAdminSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.roles.add(Role.TEACHER)
        group, created = Group.objects.get_or_create(name="Teacher")
        obj.groups.add(group)


class UserListAdminAPIView(ListAPIView):
    """User List API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector | IsAccountant | IsCashier]
    serializer_class = UserListAdminSerializer
    queryset = User.objects.all().order_by("-id")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]
    filterset_class = UserAdminFilter
    pagination_class = StandardResultsSetPagination


class UserStudentListAdminAPIView(UserListAdminAPIView):
    """Student User List API View."""

    queryset = User.objects.filter(roles__in=[Role.STUDENT]).order_by("-id")
    filterset_class = StudentAdminFilter


class UserTeacherListAdminAPIView(UserListAdminAPIView):
    queryset = User.objects.filter(roles__in=[Role.TEACHER]).order_by("-id")
    filterset_class = UserAdminFilter


class UserFacultyListAdminAPIView(UserListAdminAPIView):
    queryset = User.objects.filter(
        roles__in=tuple_to_list_first_elements(Role.staff_choices)
    )
    filterset_class = FacultyAdminFilter


class UserTrackableListAdminAPIView(UserListAdminAPIView):
    queryset = User.objects.filter(
        roles__in=tuple_to_list_first_elements(Role.trackable_staff_choices)
    )
    filterset_class = FacultyAdminFilter


class UserCounsellorListAdminAPIView(UserListAdminAPIView):
    queryset = User.objects.filter(roles__in=[Role.COUNSELLOR])
    serializer_class = UserMiniAdminSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]


class UserStudentAdminCardAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector]
    queryset = User.objects.filter(roles__in=[Role.STUDENT])

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        category = CourseCategory.objects.all()
        data = [{"title": "Overall", "data": queryset.count()}]
        data.extend(
            {
                "title": cat.name,
                "data": queryset.filter(enrolls__courses__category=cat)
                .distinct()
                .count(),
            }
            for cat in category
        )
        return Response(data)


class UserRetrieveAdminAPIView(RetrieveAPIView):
    """User Retrieve API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = UserRetrieveAdminSerializer
    queryset = User.objects.all()


class UserUpdateAdminAPIView(UpdateAPIView):
    """User Update API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]
    serializer_class = UserUpdateAdminSerializer
    queryset = User.objects.all()


class GetSMSCreditAdminAPIView(GenericAPIView):
    """Check credit of SMS provider."""

    serializer_class = SMSCreditAdminSerializer
    permission_classes = [IsAdminOrSuperAdminOrDirector]

    def get(self, request, *args, **kwargs):
        otp = OTP().getCredit()
        serializer = self.get_serializer(otp)
        return Response(serializer.data)
