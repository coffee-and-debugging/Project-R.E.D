from django.db import models
from users.models import User

class DonationRecord(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_records')
    blood_group = models.CharField(max_length=3)
    amount_ml = models.PositiveIntegerField()
    hospital_name = models.CharField(max_length=255)
    patient_saved = models.BooleanField(default=False)
    donation_date = models.DateTimeField(auto_now_add=True)
    points_earned = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.donor.username} - {self.donation_date.date()}"

class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Font awesome or emoji
    points_required = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    total_donations = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    lives_saved = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_points', '-total_donations']

    def __str__(self):
        return f"{self.user.username}: {self.total_points} points"