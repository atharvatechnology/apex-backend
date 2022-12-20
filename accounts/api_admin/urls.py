from django.urls import path

from accounts.api_admin.views import (
    GetSMSCreditAdminAPIView,
    UserCreateAdminAPIView,
    UserListAdminAPIView,
    UserRetrieveAdminAPIView,
    UserRolesView,
    UserStudentAdminCardAPIView,
    UserStudentCreateAdminAPIView,
    UserUpdateAdminAPIView,
)

app_name = "api.admin.accounts"

urlpatterns = [
    path("create/", UserCreateAdminAPIView.as_view(), name="create"),
    path(
        "create/student/",
        UserStudentCreateAdminAPIView.as_view(),
        name="student-create",
    ),
    path("card/", UserStudentAdminCardAPIView.as_view(), name="card"),
    path("list/", UserListAdminAPIView.as_view(), name="list"),
    path("retrieve/<int:pk>/", UserRetrieveAdminAPIView.as_view(), name="retrieve"),
    path("update/<int:pk>/", UserUpdateAdminAPIView.as_view(), name="update"),
    path("sms/credit/", GetSMSCreditAdminAPIView.as_view(), name="credit"),
    path("roles/list/", UserRolesView.as_view(), name="roles-list"),
]
