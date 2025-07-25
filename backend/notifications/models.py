from django.db import models
from users.models import User
from blood.models import PatientRequest

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('blood_request', 'Blood Request'),
        ('donation_accepted', 'Donation Accepted'),
        ('donation_completed', 'Donation Completed'),
        ('patient_saved', 'Patient Saved'),
        ('disease_risk', 'Disease Risk Alert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    related_request = models.ForeignKey(
        PatientRequest, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"