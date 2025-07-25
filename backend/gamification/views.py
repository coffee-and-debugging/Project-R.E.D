from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DonationRecord, Achievement, UserAchievement, Leaderboard
from .serializers import (
    DonationRecordSerializer, AchievementSerializer, 
    UserAchievementSerializer, LeaderboardSerializer
)

class DonationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = DonationRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DonationRecord.objects.filter(donor=self.request.user)

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()[:50]  # Top 50
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def my_rank(self, request):
        try:
            user_board = Leaderboard.objects.get(user=request.user)
            rank = Leaderboard.objects.filter(
                total_points__gt=user_board.total_points
            ).count() + 1
            serializer = self.get_serializer(user_board)
            data = serializer.data
            data['rank'] = rank
            return Response(data)
        except Leaderboard.DoesNotExist:
            return Response({'error': 'User not found in leaderboard'}, 
                          status=status.HTTP_404_NOT_FOUND)

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def my_achievements(self, request):
        user_achievements = UserAchievement.objects.filter(user=request.user)
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)
