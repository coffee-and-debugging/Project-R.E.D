from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from .models import Hospital
from .serializers import HospitalSerializer
from blood.models import DonationResponse

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get nearby hospitals based on user location"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if not lat or not lng:
            return Response({'error': 'lat and lng parameters required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.gis.geos import Point
        user_location = Point(float(lng), float(lat))
        
        nearby_hospitals = Hospital.objects.filter(
            location__distance_lte=(user_location, D(km=50))
        ).annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')
        
        serializer = self.get_serializer(nearby_hospitals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def active_donations(self, request, pk=None):
        """Get active donations for this hospital"""
        hospital = self.get_object()
        
        if not hasattr(request.user, 'hospital_admin') or \
           request.user.hospital_admin != hospital:
            return Response({'error': 'Not authorized for this hospital'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        active_donations = DonationResponse.objects.filter(
            hospital=hospital,
            accepted=True,
            completed=False
        ).select_related('donor', 'request__patient')
        
        from blood.serializers import DonationResponseSerializer
        serializer = DonationResponseSerializer(active_donations, many=True)
        return Response(serializer.data)
