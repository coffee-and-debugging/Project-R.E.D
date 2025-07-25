
from django.contrib import admin
from .models import PatientRequest, DonationResponse

@admin.register(PatientRequest)
class PatientRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'blood_group', 'amount_ml', 'status', 'created_at']
    list_filter = ['blood_group', 'status', 'created_at']
    search_fields = ['patient__username', 'address']
    readonly_fields = ['coordinates']

@admin.register(DonationResponse)
class DonationResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor', 'request', 'accepted', 'completed', 'hospital']
    list_filter = ['accepted', 'completed', 'created_at']
    search_fields = ['donor__username', 'request__patient__username']