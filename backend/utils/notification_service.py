import requests
from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification

class NotificationService:
    @staticmethod
    def create_notification(user, title, message, notification_type, related_request=None):
        """Create in-app notification"""
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_request=related_request
        )

    @staticmethod
    def send_email_notification(user, subject, message):
        """Send email notification"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False

    @staticmethod
    def send_push_notification(user, title, body, data=None):
        """Send push notification via FCM (you'll need to implement FCM)"""
        # TODO: Implement FCM push notifications
        # You'll need to store FCM tokens in User model
        pass

    @staticmethod
    def send_sms_notification(user, message):
        """Send SMS notification (implement with Twilio or similar)"""
        # TODO: Implement SMS notifications
        # You'll need to add phone number validation and SMS service
        pass

