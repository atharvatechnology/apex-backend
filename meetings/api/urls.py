from django.urls import path

# from . import views
from .views import GenerateSignatureAPIView, MeetingListView, zoom_webhook

urlpatterns = [
    path("signature/", GenerateSignatureAPIView.as_view(), name="generate-signature"),
    path("list/", MeetingListView.as_view(), name="meeting-list"),
    path("webhook/", zoom_webhook, name="webhook"),
]
