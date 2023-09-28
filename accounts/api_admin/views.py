from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
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
    UserTrackableListSerializer,
    UserUpdateAdminSerializer,
)
from accounts.models import Role
from common.api.views import BaseReportGeneratorAPIView
from common.paginations import StandardResultsSetPagination
from common.permissions import (
    IsAccountant,
    IsAdminOrSuperAdminOrDirector,
    IsCashier,
    IsCounsellor,
)
from common.utils import tuple_to_list, tuple_to_list_first_elements
from courses.models import CourseCategory

User = get_user_model()


class UserRolesView(APIView):
    """Roles List API View."""

    permission_classes = [IsAdminOrSuperAdminOrDirector]

    def get(self, request):
        user = request.user
        if user.is_super_admin:
            tuple_list = tuple_to_list(Role.super_admin_choices)
        elif user.is_admin:
            tuple_list = tuple_to_list(Role.admin_choices)
        elif user.is_director:
            tuple_list = tuple_to_list(Role.director_choices)
        else:
            tuple_list = []
        return Response(tuple_list)


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
    """Teacher User List API View."""

    # TODO: probably permission must be changed to IsAdminOrSuperAdminOrDirector

    queryset = User.objects.filter(roles__in=[Role.TEACHER]).order_by("-id")
    filterset_class = UserAdminFilter


class UserFacultyListAdminAPIView(UserListAdminAPIView):
    """Faculty User List API View."""

    # TODO: probably permission must be changed to IsAdminOrSuperAdminOrDirector

    queryset = User.objects.filter(
        roles__in=tuple_to_list_first_elements(Role.staff_choices)
    )
    filterset_class = FacultyAdminFilter


class UserTrackableListAdminAPIView(UserListAdminAPIView):
    """Trackable User List API View."""

    # TODO: probably permission must be changed to IsAdminOrSuperAdminOrDirector

    queryset = User.objects.filter(
        roles__in=tuple_to_list_first_elements(Role.trackable_staff_choices)
    )
    filterset_class = FacultyAdminFilter
    serializer_class = UserTrackableListSerializer


class UserCounsellorListAdminAPIView(UserListAdminAPIView):
    permission_classes = [IsAdminOrSuperAdminOrDirector | IsCashier | IsCounsellor]
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


class StudentReportGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["username", "first_name", "last_name"]
    queryset = User.objects.filter(roles__in=[Role.STUDENT]).order_by("-id")
    filterset_class = StudentAdminFilter
    model_name = "StudentProfile"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "fullname",
                    "date_joined",
                    "phone_number",
                    "email",
                    "status",
                    "college_name",
                    "address",
                ]
            }
        )


class TeacherReportGeneratorAPIView(BaseReportGeneratorAPIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["username", "first_name", "last_name"]
    queryset = User.objects.filter(roles__in=[Role.TEACHER]).order_by("-id")
    filterset_class = UserAdminFilter
    model_name = "TeacherProfile"

    def get(self, request):
        return Response(
            {
                "model_fields": [
                    "fullname",
                    "phone_number",
                    "email",
                ]
            }
        )


class RegenerateQRCodeAdminAPIView(APIView):
    """API endpoint to regenerate QR code for a user profile.

    This API view is accessible only to users with the IsAdminOrSuperAdminOrDirector
    permission class. It regenerates the QR code for a user's profile by calling the
    generate_qr_code method of the user's Profile instance. The user's ID is taken
    from the URL parameters and used to retrieve the user object from the database.

    Returns
        Response: A JSON response with a success message.

    """

    permission_classes = [IsAdminOrSuperAdminOrDirector]

    def post(self, request, *args, **kwargs):
        """Regenerate a QR code for a user's profile.

        Args:
            request: The HTTP request object.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns
            A Response object with a success message.

        """
        user_id = self.kwargs.get("pk")
        user = get_object_or_404(User, id=user_id)
        user.profile.generate_qr_code()
        return Response({"message": "QR Code Regenerated"})
