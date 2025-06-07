from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models

class User(AbstractUser):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    allergies = models.TextField(blank=True)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    is_donor = models.BooleanField(default=True)  # default donor
    is_patient = models.BooleanField(default=False)
    location = gis_models.PointField(geography=True, blank=True, null=True)

    def __str__(self):
        return self.username
