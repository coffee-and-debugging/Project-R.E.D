from twilio.rest import Client
from django.conf import settings

class SMSService:
    @staticmethod
    def send_sms(phone_number, message):
        """Send SMS using Twilio"""
        if not all([
            hasattr(settings, 'TWILIO_ACCOUNT_SID'),
            hasattr(settings, 'TWILIO_AUTH_TOKEN'),
            hasattr(settings, 'TWILIO_PHONE_NUMBER')
        ]):
            print("Twilio credentials not configured")
            return False
            
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return True
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False
