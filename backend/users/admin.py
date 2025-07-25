from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'blood_group', 'is_donor', 'is_patient', 'dob']
    list_filter = ['blood_group', 'is_donor', 'is_patient', 'sex']
    search_fields = ['username', 'email', 'contact']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('blood_group', 'allergies', 'dob', 'sex', 'address', 
                      'contact', 'is_donor', 'is_patient', 'location', 'fcm_token',
                      'occupation', 'suffers_any_disease',
                      'ever_tested_hiv_positive', 'cardiac_problems', 'bleeding_disorders',
                      'donated_blood_before', 'takes_medication')
        }),
    )