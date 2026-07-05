from django.contrib import admin
from .models import MedicalProfile, EmergencyContact

admin.site.register(MedicalProfile)
admin.site.register(EmergencyContact)
