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
    
    SEX = [
        ("Male", "M"),
        ("Female", "F"),
        ("Others", "O"),
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    allergies = models.TextField(blank=True)
    dob = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    is_donor = models.BooleanField(default=True)
    is_patient = models.BooleanField(default=False)
    location = gis_models.PointField(geography=True, blank=True, null=True)
    fcm_token = models.TextField(blank=True, null=True)
    
    occupation = models.CharField(max_length=100, blank=True, null=True)
    suffers_any_disease = models.BooleanField(default=False)
    ever_tested_hiv_positive = models.BooleanField(default=False)
    cardiac_problems = models.BooleanField(default=False)
    bleeding_disorders = models.BooleanField(default=False)
    donated_blood_before = models.BooleanField(default=False)
    takes_medication = models.BooleanField(default=False)

    def __str__(self):
        return self.username
