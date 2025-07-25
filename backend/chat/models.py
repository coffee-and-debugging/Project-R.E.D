# chat/models.py
from django.db import models
from users.models import User
from blood.models import PatientRequest, DonationResponse

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    donation_response = models.OneToOneField(
        DonationResponse, 
        on_delete=models.CASCADE, 
        related_name='chat_room'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.name}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"