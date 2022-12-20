from django.urls import include, path

from accounts.api_admin.views import (
    GetSMSCreditAdminAPIView,
    UserCreateAdminAPIView,
    UserListAdminAPIView,
    UserRetrieveAdminAPIView,
    UserRolesView,
    UserStudentAdminCardAPIView,
    UserStudentCreateAdminAPIView,
    UserStudentListAdminAPIView,
    UserTeacherListAdminAPIView,
    UserUpdateAdminAPIView,
)

app_name = "api.admin.accounts"

student_url = [
    path(
        "create/",
        UserStudentCreateAdminAPIView.as_view(),
        name="student-create",
    ),
    path("card/", UserStudentAdminCardAPIView.as_view(), name="card"),
    path("list/", UserStudentListAdminAPIView.as_view(), name="list"),
]

teacher_url = [
    path("list/", UserTeacherListAdminAPIView.as_view(), name="list"),
]

urlpatterns = [
    path("create/", UserCreateAdminAPIView.as_view(), name="create"),
    path("student/", include(student_url)),
    path("teacher/", include(teacher_url)),
    path("list/", UserListAdminAPIView.as_view(), name="list"),
    path("retrieve/<int:pk>/", UserRetrieveAdminAPIView.as_view(), name="retrieve"),
    path("update/<int:pk>/", UserUpdateAdminAPIView.as_view(), name="update"),
    path("sms/credit/", GetSMSCreditAdminAPIView.as_view(), name="credit"),
    path("roles/list/", UserRolesView.as_view(), name="roles-list"),
]
