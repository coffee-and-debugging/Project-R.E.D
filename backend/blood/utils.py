from utils.notification_service import NotificationService

def send_notification(user, message, request_id, notification_type='blood_request'):
    """Enhanced notification function"""
   
    NotificationService.create_notification(
        user=user,
        title="Blood Request Alert 🚨",
        message=message,
        notification_type=notification_type,
        related_request_id=request_id
    )
    
    
    NotificationService.send_email_notification(
        user=user,
        subject="Urgent Blood Request Alert 🚨",
        message=f"{message}\n\nView request: https://yourapp.com/request/{request_id}"
    )
    
    # TODO: Add push notification when implemented
    # NotificationService.send_push_notification(user, "Blood Request", message)
