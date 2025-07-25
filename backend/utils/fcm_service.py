import requests
import json
from django.conf import settings

class FCMService:
    @staticmethod
    def send_push_notification(fcm_token, title, body, data=None):
        """Send push notification using FCM"""
        if not hasattr(settings, 'FCM_SERVER_KEY'):
            print("FCM_SERVER_KEY not configured")
            return False
            
        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': f'key={settings.FCM_SERVER_KEY}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'to': fcm_token,
            'notification': {
                'title': title,
                'body': body,
                'sound': 'default'
            },
            'data': data or {}
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            return response.status_code == 200
        except Exception as e:
            print(f"FCM notification failed: {e}")
            return False