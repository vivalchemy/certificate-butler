from django.db import models
import random
import string


# generates the random certificate code
def randomCertificateTemplateCode(length=6):
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if CertificateTemplate.objects.filter(code=code).count() == 0:
            break
    return code


# generates the random participant code
def randomParticipantCode(length=8):
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if Participant.objects.filter(code=code).count() == 0:
            break
    return code


# Create your models here.
# Stores the templates of the certificates and other details
class CertificateTemplate(models.Model):

    code = models.CharField(
        max_length=6, primary_key=True, default=randomCertificateTemplateCode
    )
    competitionName = models.CharField(max_length=100)
    fontSize = models.IntegerField()
    fontFamily = models.CharField(max_length=100)
    textPosition = models.FloatField()
    image = models.ImageField(upload_to="certificate-templates/")
    csv = models.FileField(upload_to="csv/", blank=True)

    def __str__(self):
        return f"{self.competitionName}:{self.code}"

    def save(self, *args, **kwargs):
        super(CertificateTemplate, self).save(*args, **kwargs)


# Stores the participant details
class Participant(models.Model):

    code = models.CharField(
        max_length=8, primary_key=True, default=randomParticipantCode
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    # certificate = models.ImageField(upload_to="certificates/")
    certificateTemplate = models.ForeignKey(
        CertificateTemplate, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}:{self.code}"
