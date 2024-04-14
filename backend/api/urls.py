from django.urls import path
from .views import CertificateTemplateView, ParticipantView, ZippedImagesView

urlpatterns = [
    path("certificate-templates/", CertificateTemplateView.as_view()),
    path("participants/", ParticipantView.as_view()),
    path("zipped-images/", ZippedImagesView.as_view()),
]
