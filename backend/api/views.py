from rest_framework import generics, status
from rest_framework.response import Response
from .models import CertificateTemplate, Participant, ZippedImages
from .serializers import (
    CertificateTemplateSerializer,
    ParticipantSerializer,
    ZippedImagesSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser

# extras
from .utils.csv_parser import parseCSV
from .utils.imageGen import generateCertificate
from .utils.zipGen import generateZip
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse


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

            # Parsing
            csv_file = certificate_template.csv
            csv_content = parseCSV(csv_file)
            participants = []
            for row in csv_content:
                certificateInBytes = generateCertificate(
                    certificate_template.image.path,
                    row.get("name", ""),
                    certificate_template.fontSize,
                    certificate_template.textPosition,
                )
                # certificate = InMemoryUploadedFile(
                #     certificateInBytes,
                #     None,
                #     f"{certificate_template.competitionName}-{row.get('name', '').replace(' ', '_')}.{certificate_template.image.name.split('.')[-1]}",
                #     f"image/{certificate_template.image.name.split('.')[-1]}",
                #     certificateInBytes.tell(),
                #     None,
                # )
                certificate = SimpleUploadedFile(
                    name=f"{certificate_template.competitionName.replace(' ', '_')}-{row.get('name', '').replace(' ', '_')}.{certificate_template.image.name.split('.')[-1]}",
                    content=certificateInBytes.read(),
                    content_type=f"image/{certificate_template.image.name.split('.')[-1]}",
                )
                participant_data = {
                    "name": row.get("name", ""),
                    "email": row.get("email", ""),
                    "certificate": certificate,
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

            # Zipping
            zipBytes = generateZip(participants)
            zipFile = SimpleUploadedFile(
                name=f"{certificate_template.competitionName.replace(' ', '_')}.zip",
                content=zipBytes.read(),
                content_type="application/zip",
            )
            zipData = {
                "zipFile": zipFile,
                "certificateTemplate": certificate_template.code,
            }
            zipped_images_serializer = ZippedImagesSerializer(data=zipData)
            if zipped_images_serializer.is_valid():
                zipped_images = zipped_images_serializer.save()
                print("Zipped Images: ", zipped_images)
            else:
                return Response(
                    zipped_images_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "message": "Certificates and Participants and zip created successfully",
                    "code": certificate_template.code,
                },
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

    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return Response(
                {"error": "Certificate Id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        participants = Participant.objects.filter(certificateTemplate=id)
        response = []
        for participant in participants:
            code = participant.code
            name = participant.name
            email = participant.email
            href = participant.certificate.url
            response.append({"code": code, "name": name, "email": email, "href": href})

        return JsonResponse({"data": response})


class ZippedImagesView(generics.ListCreateAPIView):
    queryset = ZippedImages.objects.all()
    serializer_class = ZippedImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request):
        # Check if the files are valid or not
        if "zipFile" not in request.FILES:
            return Response(
                {"error": "No Zip file generated"}, status=status.HTTP_400_BAD_REQUEST
            )
        uploaded_zip_file = request.FILES["zipFile"]
        if uploaded_zip_file.content_type != "application/zip":
            return Response(
                {"error": "Unsupported file type. Please upload a valid CSV file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return Response(
                {"error": "Certificate Id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        zippedImages = ZippedImages.objects.filter(certificateTemplate=id)
        response = []
        for file in zippedImages:
            href = file.zipFile.url
            code = file.code
            response.append({"href": href, "code": code})

        return JsonResponse({"data": response})
