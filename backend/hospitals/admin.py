from django.contrib import admin
from .models import Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'contact', 'admin']
    search_fields = ['name', 'address', 'admin__username']
    readonly_fields = ['location']
