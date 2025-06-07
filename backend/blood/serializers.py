from rest_framework_gis.serializers import GeometryField
from rest_framework import serializers
from .models import PatientRequest, DonationResponse

class PatientRequestSerializer(serializers.ModelSerializer):
    coordinates = GeometryField()

    class Meta:
        model = PatientRequest
        fields = '__all__'
        read_only_fields = ['patient', 'status', 'created_at']

    # def validate_coordinates(self, value):
    #     if value.geom_type != 'Point':
    #         raise serializers.ValidationError("Only Point geometry is allowed.")
    #     return value

class DonationResponseSerializer(serializers.ModelSerializer):
    donor_location = GeometryField(required=False, allow_null=True)
    class Meta:
        model = DonationResponse
        fields = '__all__'
        read_only_fields = ['donor', 'created_at']
