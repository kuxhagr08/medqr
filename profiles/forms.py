from django import forms
from .models import MedicalProfile, EmergencyContact

class MedicalProfileForm(forms.ModelForm):
    class Meta:
        model = MedicalProfile
        fields = ['blood_group', 'allergies', 'medical_conditions', 'medications']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relation', 'phone', 'email']
