from django.urls import path

from accounts.api_admin.views import (
    GetSMSCreditAdminAPIView,
    UserCreateAdminAPIView,
    UserListAdminAPIView,
    UserRetrieveAdminAPIView,
    UserUpdateAdminAPIView,
)

app_name = "api.admin.accounts"

urlpatterns = [
    path("create/", UserCreateAdminAPIView.as_view(), name="create"),
    path("list/", UserListAdminAPIView.as_view(), name="list"),
    path("retrieve/<int:pk>/", UserRetrieveAdminAPIView.as_view(), name="retrieve"),
    path("update/<int:pk>/", UserUpdateAdminAPIView.as_view(), name="update"),
    path("sms/credit/", GetSMSCreditAdminAPIView.as_view(), name="credit"),
]
