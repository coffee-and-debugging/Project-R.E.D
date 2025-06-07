from django.db import models
from django.contrib.gis.db import models as gis_models
from users.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    location = gis_models.PointField(geography=True, blank=True, null=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_admin')

    def __str__(self):
        return self.name
