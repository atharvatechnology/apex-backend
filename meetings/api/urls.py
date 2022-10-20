from django.urls import path

# from . import views
from .views import GenerateSignatureAPIView, MeetingListView

urlpatterns = [
    path("signature/", GenerateSignatureAPIView.as_view(), name="generate-signature"),
    path("list/", MeetingListView.as_view(), name="meeting-list"),
]
