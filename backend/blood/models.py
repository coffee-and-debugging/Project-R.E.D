from django.db import models
from django.contrib.gis.db import models as gis_models
from users.models import User
from hospitals.models import Hospital

class PatientRequest(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_requests')
    blood_group = models.CharField(max_length=3)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    amount_ml = models.PositiveIntegerField()
    coordinates = gis_models.PointField(geography=True)
    status = models.CharField(max_length=20, default='pending')  # pending, accepted, completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.patient.username} for {self.blood_group}"

class DonationResponse(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_responses')
    request = models.ForeignKey(PatientRequest, on_delete=models.CASCADE, related_name='donation_responses')
    accepted = models.BooleanField(default=False)
    donor_location = gis_models.PointField(geography=True, blank=True, null=True)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.SET_NULL)
    chat_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.donor.username} to Request {self.request.id}"
