from django.contrib import admin
from .models import DonationRecord, Achievement, UserAchievement, Leaderboard

@admin.register(DonationRecord)
class DonationRecordAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_group', 'amount_ml', 'hospital_name', 'patient_saved', 'donation_date']
    list_filter = ['blood_group', 'patient_saved', 'donation_date']
    search_fields = ['donor__username', 'hospital_name']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'icon']
    search_fields = ['name', 'description']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['user__username', 'achievement__name']

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_donations', 'total_points', 'lives_saved', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__username']
    ordering = ['-total_points']