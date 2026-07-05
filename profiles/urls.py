from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('contact/add/', views.add_contact, name='add_contact'),
    path('emergency/<uuid:uuid>/', views.emergency_view, name='emergency_view'),
]
