import uuid
from django.db import models
from django.contrib.auth.models import User

class MedicalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medical_profile')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    blood_group = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True, help_text="List any allergies separated by commas")
    medical_conditions = models.TextField(blank=True, help_text="E.g., Diabetes, Asthma")
    medications = models.TextField(blank=True, help_text="Current medications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Medical Profile"

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.relation})"
