from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'blood_group', 'allergies', 'dob', 'sex', 'address', 'contact',
            'is_donor', 'is_patient', 'location', 'fcm_token', 'occupation', 'suffers_any_disease',
            'ever_tested_hiv_positive', 'cardiac_problems', 'bleeding_disorders',
            'donated_blood_before', 'takes_medication',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
