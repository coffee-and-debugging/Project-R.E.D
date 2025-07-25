from rest_framework.routers import DefaultRouter
from .views import DonationRecordViewSet, LeaderboardViewSet, AchievementViewSet

router = DefaultRouter()
router.register(r'donations', DonationRecordViewSet, basename='donations')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'achievements', AchievementViewSet, basename='achievements')

urlpatterns = router.urls
