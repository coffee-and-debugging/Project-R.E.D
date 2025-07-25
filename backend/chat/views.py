# chat/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from django.db import models


class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see chat rooms where they are donor or patient
        return ChatRoom.objects.filter(
            models.Q(donation_response__donor=self.request.user) |
            models.Q(donation_response__request__patient=self.request.user)
        )

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        room = self.get_object()
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def close_chat(self, request, pk=None):
        room = self.get_object()
        room.is_active = False
        room.save()
        return Response({'status': 'chat closed'})