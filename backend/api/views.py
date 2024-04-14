from rest_framework import generics, status
from rest_framework.response import Response
from .models import CertificateTemplate, Participant
from .serializers import CertificateTemplateSerializer, ParticipantSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# extras
from .utils.csv_parser import parseCSV
from django.conf import settings

class CertificateTemplateView(generics.ListCreateAPIView):
    queryset = CertificateTemplate.objects.all()
    serializer_class = CertificateTemplateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        # Check if the files are valid or not
        if "csv" not in request.FILES:
            return Response(
                {"error": "No CSV file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        if "image" not in request.FILES:
            return Response(
                {"error": "No Certificate Template provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the uploaded file is an image
        uploaded_csv_file = request.FILES["csv"]
        uploaded_image_file = request.FILES["image"]
        allowed_image_types = [
            "image/jpeg",
            "image/png",
        ]  # Add more as needed

        if uploaded_csv_file.content_type != "text/csv":
            return Response(
                {"error": "Unsupported file type. Please upload a valid CSV file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if uploaded_image_file.content_type not in allowed_image_types:
            return Response(
                {
                    "error": "Unsupported file type. Please upload a valid image file(JPG, PNG, JPEG)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse CSV file
        # csv_reader = parseCSV(uploaded_csv_file)
        # print("CSV Reader: ", csv_reader)

        certificate_template_serializer = CertificateTemplateSerializer(
            data=request.data
        )

        if certificate_template_serializer.is_valid():
            certificate_template = certificate_template_serializer.save()

            #Parsing
            csv_file = certificate_template.csv
            csv_content = parseCSV(csv_file)
            print("Exiting parsing")
            print(csv_content)
            print("Exiting content")
            participants = []
            for row in csv_content:
                print(row)
                participant_data = {
                    "name": row.get("name", ""),
                    "email": row.get("email", ""),
                    "certificateTemplate": certificate_template.code,
                }
                participant_serializer = ParticipantSerializer(data=participant_data)
                if participant_serializer.is_valid():
                    participant = participant_serializer.save()
                    participants.append(participant)
                else:
                    return Response(
                        participant_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"message": "Certificates and Participants created successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Certificates created successfully"},
            status=status.HTTP_201_CREATED,
        )


class ParticipantView(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    parser_classes = (MultiPartParser, FormParser)
