from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from .serializers import UserRegistrationSerializer
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_location(self, request):
        """Update user location"""
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        
        if not lat or not lng:
            return Response({'error': 'lat and lng required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        request.user.location = Point(float(lng), float(lat))
        request.user.save()
        
        return Response({'status': 'location updated'})

    @action(detail=False, methods=['post'])
    def toggle_donor_status(self, request):
        """Toggle donor availability"""
        request.user.is_donor = not request.user.is_donor
        request.user.save()
        
        return Response({
            'status': 'donor status updated',
            'is_donor': request.user.is_donor
        })
