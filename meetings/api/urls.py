from django.urls import path

# from . import views
from .views import GenerateSignatureAPIView

urlpatterns = [
    path("signature/", GenerateSignatureAPIView.as_view(), name="generate-signature"),
]
