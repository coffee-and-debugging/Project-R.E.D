from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from .models import PatientRequest, DonationResponse
from .serializers import PatientRequestSerializer, DonationResponseSerializer
from users.models import User
from hospitals.models import Hospital
from .ml_service import predict_hospital, assess_disease_risk


class PatientRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PatientRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientRequest.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        # DO NOT manually parse coordinates anymore
        point = serializer.validated_data['coordinates']  # already parsed from GeoJSON
        serializer.save(patient=self.request.user, status='pending')

        # Now use 'point' for distance query
        donors = User.objects.filter(
            is_donor=True,
            blood_group=serializer.validated_data['blood_group']
        ).annotate(distance=Distance('location', point)).order_by('distance')[:10]

        # TODO: Send notifications to these donors


class DonationResponseViewSet(viewsets.ModelViewSet):
    serializer_class = DonationResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DonationResponse.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        coords = data.get('donor_location')
        if not coords or 'lat' not in coords or 'lng' not in coords:
            raise ValidationError("Donor location coordinates are required.")
        point = Point(float(coords['lng']), float(coords['lat']))

        # Predict hospital using ML model
        hospital = predict_hospital(data)

        serializer.save(donor=self.request.user, donor_location=point, hospital=hospital, accepted=True, chat_active=True)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        if data.get('completed', False):
            # Use ML to assess disease risk after donation
            risk = assess_disease_risk({'donor_id': instance.donor.id})
            # TODO: Notify donor if risk detected

            instance.completed = True
            instance.chat_active = False
            instance.save()

        return super().update(request, *args, **kwargs)
