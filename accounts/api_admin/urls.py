from django.urls import path

from accounts.api_admin.views import UserListAPIView

app_name = "accounts"

urlpatterns = [
    path("list/", UserListAPIView.as_view(), name="admin-list"),
]
