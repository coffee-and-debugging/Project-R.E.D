from gamification.models import Achievement, UserAchievement, Leaderboard
from utils.notification_service import NotificationService

class AchievementService:
    @staticmethod
    def check_and_award_achievements(user):
        """Check if user has earned any new achievements"""
        try:
            leaderboard = Leaderboard.objects.get(user=user)
        except Leaderboard.DoesNotExist:
            return

        earned_achievement_ids = UserAchievement.objects.filter(
            user=user
        ).values_list('achievement_id', flat=True)
        
        available_achievements = Achievement.objects.exclude(
            id__in=earned_achievement_ids
        )

        for achievement in available_achievements:
            earned = False
            
            if achievement.name == 'First Drop' and leaderboard.total_donations >= 1:
                earned = True
            elif achievement.name == 'Life Saver' and leaderboard.lives_saved >= 1:
                earned = True
            elif achievement.name == 'Hero' and leaderboard.total_donations >= 5:
                earned = True
            elif achievement.name == 'Champion' and leaderboard.total_donations >= 10:
                earned = True
            elif achievement.name == 'Legend' and leaderboard.total_donations >= 25:
                earned = True
            elif achievement.name == 'Guardian Angel' and leaderboard.lives_saved >= 5:
                earned = True
            
            if earned:
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement
                )
                
                NotificationService.create_notification(
                    user=user,
                    title=f"Achievement Unlocked! {achievement.icon}",
                    message=f"You've earned the '{achievement.name}' achievement! {achievement.description}",
                    notification_type='achievement'
                )
