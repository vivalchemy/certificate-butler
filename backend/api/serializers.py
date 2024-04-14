from rest_framework.serializers import ModelSerializer
from .models import CertificateTemplate, Participant


class CertificateTemplateSerializer(ModelSerializer):

    class Meta:
        model = CertificateTemplate
        fields = "__all__"
        read_only_fields = ["code"]


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"
        read_only_fields = ["code"]
