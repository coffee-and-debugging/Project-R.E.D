from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'user_name', 'timestamp', 'is_read']
        read_only_fields = ['user', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_active', 'messages', 'created_at']