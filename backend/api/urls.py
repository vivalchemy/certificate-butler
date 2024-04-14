from django.urls import path
from .views import CertificateTemplateView, ParticipantView

urlpatterns = [
    path("certificate-templates/", CertificateTemplateView.as_view()),
    path("participants/", ParticipantView.as_view()),
]
