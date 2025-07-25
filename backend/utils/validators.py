from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    """Validate phone number format"""
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number format')

def validate_blood_group(value):
    """Validate blood group"""
    valid_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    if value not in valid_groups:
        raise ValidationError('Invalid blood group')