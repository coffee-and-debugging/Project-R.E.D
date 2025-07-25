# blood/views.py (Updated with complete functionality)
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db import models

from .models import PatientRequest, DonationResponse
from .serializers import PatientRequestSerializer, DonationResponseSerializer
from users.models import User
from hospitals.models import Hospital
from chat.models import ChatRoom
from gamification.models import DonationRecord, Leaderboard
from .ml_service import predict_hospital, assess_disease_risk
from .utils import send_notification
from utils.notification_service import NotificationService

class PatientRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PatientRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientRequest.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        point = serializer.validated_data['coordinates']
        request = serializer.save(patient=self.request.user, status='pending')

        self.request.user.is_patient = True
        self.request.user.save()

        nearby_donors = User.objects.filter(
            is_donor=True,
            blood_group=serializer.validated_data['blood_group'],
            location__distance_lte=(point, D(km=20))
        ).annotate(
            distance=Distance('location', point)
        ).order_by('distance')[:10]

        if not nearby_donors.exists():
            nearby_donors = User.objects.filter(
                is_donor=True,
                blood_group=serializer.validated_data['blood_group'],
                location__distance_lte=(point, D(km=50))
            ).annotate(
                distance=Distance('location', point)
            ).order_by('distance')[:15]

        for donor in nearby_donors:
            send_notification(
                user=donor,
                message=f"Urgent blood request for group {request.blood_group}. "
                       f"Patient needs {request.amount_ml}ml blood at {request.address}.",
                request_id=request.id,
                notification_type='blood_request'
            )

    @action(detail=True, methods=['post'])
    def cancel_request(self, request, pk=None):
        """Allow patient to cancel their request"""
        patient_request = self.get_object()
        if patient_request.status == 'pending':
            patient_request.status = 'cancelled'
            patient_request.save()
            return Response({'status': 'request cancelled'})
        return Response({'error': 'Cannot cancel non-pending request'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class DonationResponseViewSet(viewsets.ModelViewSet):
    serializer_class = DonationResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DonationResponse.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        """Donor accepts a blood request"""
        data = self.request.data
        coords = data.get('donor_location')
        
        if not coords or 'lat' not in coords or 'lng' not in coords:
            raise ValidationError("Donor location coordinates are required.")
        
        point = Point(float(coords['lng']), float(coords['lat']))
        
        patient_request = serializer.validated_data['request']
        
        ml_data = {
            'donor_lat': coords['lat'],
            'donor_lng': coords['lng'],
            'patient_lat': patient_request.coordinates.y,
            'patient_lng': patient_request.coordinates.x,
            'blood_group': patient_request.blood_group,
            'amount_ml': patient_request.amount_ml
        }
        hospital = predict_hospital(ml_data)

        donation_response = serializer.save(
            donor=self.request.user, 
            donor_location=point, 
            hospital=hospital, 
            accepted=True, 
            chat_active=True
        )

        patient_request.status = 'accepted'
        patient_request.save()

        chat_room = ChatRoom.objects.create(
            name=f"chat_{patient_request.id}_{self.request.user.id}",
            donation_response=donation_response
        )

        NotificationService.create_notification(
            user=patient_request.patient,
            title="Donor Found! 🎉",
            message=f"{self.request.user.username} has accepted your blood request. "
                   f"Hospital: {hospital.name}",
            notification_type='donation_accepted',
            related_request=patient_request
        )

        NotificationService.send_email_notification(
            user=patient_request.patient,
            subject="Donor Found for Your Blood Request!",
            message=f"Good news! {self.request.user.username} has accepted your blood request.\n"
                   f"Hospital: {hospital.name}\n"
                   f"Address: {hospital.address}\n"
                   f"Contact: {hospital.contact}"
        )

    @action(detail=True, methods=['post'])
    def complete_donation(self, request, pk=None):
        """Mark donation as completed (called by hospital admin)"""
        donation_response = self.get_object()
        
        if not hasattr(request.user, 'hospital_admin'):
            return Response({'error': 'Only hospital admin can complete donations'}, 
                           status=status.HTTP_403_FORBIDDEN)

        risk_data = {
            'donor_id': donation_response.donor.id,
            'donor_age': donation_response.donor.age,
            'blood_group': donation_response.request.blood_group,
            'allergies': donation_response.donor.allergies
        }
        
        disease_risk = assess_disease_risk(risk_data)
        
        if disease_risk:
            NotificationService.create_notification(
                user=donation_response.donor,
                title="Health Check Recommendation",
                message="Based on your recent donation, we recommend a health checkup. "
                       "Please consult with your healthcare provider.",
                notification_type='disease_risk'
            )

        donation_response.completed = True
        donation_response.chat_active = False
        donation_response.save()

        donation_response.request.status = 'completed'
        donation_response.request.save()

        points = 10
        if donation_response.request.amount_ml > 400:
            points = 15  # Bonus for larger donations

        donation_record = DonationRecord.objects.create(
            donor=donation_response.donor,
            blood_group=donation_response.request.blood_group,
            amount_ml=donation_response.request.amount_ml,
            hospital_name=donation_response.hospital.name,
            points_earned=points
        )

        leaderboard, created = Leaderboard.objects.get_or_create(
            user=donation_response.donor,
            defaults={
                'total_donations': 1,
                'total_points': points,
                'lives_saved': 0
            }
        )
        
        if not created:
            leaderboard.total_donations += 1
            leaderboard.total_points += points
            leaderboard.save()

        NotificationService.create_notification(
            user=donation_response.donor,
            title="Donation Completed! 🏆",
            message=f"Thank you for your donation! You earned {points} points. "
                   f"Total donations: {leaderboard.total_donations}",
            notification_type='donation_completed'
        )

        return Response({'status': 'donation completed', 'points_earned': points})

    @action(detail=True, methods=['post'])
    def patient_saved(self, request, pk=None):
        """Update when patient is saved (called by hospital admin)"""
        donation_response = self.get_object()
        
        if not hasattr(request.user, 'hospital_admin'):
            return Response({'error': 'Only hospital admin can update patient status'}, 
                           status=status.HTTP_403_FORBIDDEN)

        try:
            donation_record = DonationRecord.objects.get(
                donor=donation_response.donor,
                blood_group=donation_response.request.blood_group,
                hospital_name=donation_response.hospital.name
            )
            donation_record.patient_saved = True
            donation_record.save()

            leaderboard = Leaderboard.objects.get(user=donation_response.donor)
            leaderboard.lives_saved += 1
            leaderboard.total_points += 5 
            leaderboard.save()

            NotificationService.create_notification(
                user=donation_response.donor,
                title="Life Saved! 🌟",
                message="Amazing news! Your blood donation helped save a life. "
                       f"You've now saved {leaderboard.lives_saved} lives!",
                notification_type='patient_saved'
            )

            return Response({
                'status': 'patient saved updated', 
                'lives_saved': leaderboard.lives_saved
            })
        
        except DonationRecord.DoesNotExist:
            return Response({'error': 'Donation record not found'}, 
                           status=status.HTTP_404_NOT_FOUND)

