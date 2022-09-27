from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"devices", FCMDeviceAuthorizedViewSet)

from meetings.api_admin.urls import subject_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

api_urls = [
    path("accounts/", include("accounts.api.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("courses/", include("courses.api.urls")),
    path("notes/", include("notes.api.urls")),
    path("exams/", include("exams.api.urls")),
    path("enrollments/", include("enrollments.api.urls")),
    path("physical-book/", include("physicalbook.api.urls")),
    path("attendance/", include("attendance.api.urls")),
    path("meetings/", include("meetings.api.urls")),
    path("payments/", include("payments.api.urls")),
]

api_admin_urls = [
    path("exams/", include("exams.api_admin.urls")),
    path("courses/", include("courses.api_admin.urls")),
    path("notes/", include("notes.api_admin.urls")),
    path("enrollments/", include("enrollments.api_admin.urls")),
    path("accounts/", include("accounts.api_admin.urls")),
    path("meetings/", include("meetings.api_admin.urls")),
    path("subjects/", include(subject_urlpatterns)),
]

fcm_urls = [
    path("", include(router.urls)),
    path("send/", include("notifications.api_admin.urls")),
]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("api/admin/", include(api_admin_urls)),
    path("api/fcm/", include(fcm_urls)),
    # path("student_urls/", include("student.api.urls")),
    # path("teacher_urls/", include("teacher.api.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
