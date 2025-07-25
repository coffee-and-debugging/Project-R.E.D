# gamification/serializers.py
from rest_framework import serializers
from .models import DonationRecord, Achievement, UserAchievement, Leaderboard

class DonationRecordSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.username', read_only=True)
    
    class Meta:
        model = DonationRecord
        fields = '__all__'
        read_only_fields = ['donor', 'donation_date', 'points_earned']

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement_details = AchievementSerializer(source='achievement', read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['achievement_details', 'earned_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['user_id', 'username', 'total_donations', 'total_points', 'lives_saved']