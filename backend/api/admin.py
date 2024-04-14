from django.contrib import admin
from .models import CertificateTemplate, Participant, ZippedImages

admin.site.register(CertificateTemplate)
admin.site.register(Participant)
admin.site.register(ZippedImages)

# Register your models here.
