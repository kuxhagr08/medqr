from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import MedicalProfile, EmergencyContact
from .forms import MedicalProfileForm, EmergencyContactForm
from django.core.mail import send_mail
from django.http import JsonResponse
import json
import qrcode
from io import BytesIO
import base64

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'profiles/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a medical profile for the new user
            MedicalProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.medical_profile
    contacts = request.user.emergency_contacts.all()
    
    # Generate QR Code for the user's emergency URL
    # Using request.build_absolute_uri to get the full domain
    emergency_url = request.build_absolute_uri(f'/emergency/{profile.uuid}/')
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(emergency_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'profile': profile,
        'contacts': contacts,
        'qr_image': qr_image_base64,
        'emergency_url': emergency_url
    }
    return render(request, 'profiles/dashboard.html', context)

@login_required
def update_profile(request):
    profile = request.user.medical_profile
    if request.method == 'POST':
        form = MedicalProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MedicalProfileForm(instance=profile)
    return render(request, 'profiles/form_view.html', {'form': form, 'title': 'Update Medical Profile'})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('dashboard')
    else:
        form = EmergencyContactForm()
    return render(request, 'profiles/form_view.html', {'form': form, 'title': 'Add Emergency Contact'})

def emergency_view(request, uuid):
    profile = get_object_or_404(MedicalProfile, uuid=uuid)
    contacts = profile.user.emergency_contacts.all()
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('lat')
            lng = data.get('lng')
            
            if not lat or not lng:
                return JsonResponse({'status': 'error', 'message': 'Location missing'}, status=400)
                
            map_url = f"https://www.google.com/maps?q={lat},{lng}"
            subject = f"EMERGENCY ALERT: {profile.user.username} needs help!"
            message = f"An emergency has been reported for {profile.user.first_name} {profile.user.last_name}.\n\n"
            message += f"Current Location: {map_url}\n\n"
            message += f"Medical Conditions: {profile.medical_conditions}\n"
            message += f"Allergies: {profile.allergies}\n"
            message += f"Blood Group: {profile.blood_group}\n\n"
            message += "Please reach out to them or send help immediately."
            
            recipient_list = [contact.email for contact in contacts if contact.email]
            
            if recipient_list:
                send_mail(
                    subject,
                    message,
                    'alerts@medqr.com',
                    recipient_list,
                    fail_silently=False,
                )
            
            return JsonResponse({'status': 'success', 'message': 'Contacts notified.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'profiles/emergency_view.html', {'profile': profile})


