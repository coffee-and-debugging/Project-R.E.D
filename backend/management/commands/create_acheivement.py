from django.core.management.base import BaseCommand
from gamification.models import Achievement

class Command(BaseCommand):
    help = 'Create default achievements'

    def handle(self, *args, **options):
        achievements = [
            {
                'name': 'First Drop',
                'description': 'Made your first blood donation',
                'icon': '🩸',
                'points_required': 0
            },
            {
                'name': 'Life Saver',
                'description': 'Saved your first life',
                'icon': '💝',
                'points_required': 10
            },
            {
                'name': 'Hero',
                'description': 'Made 5 blood donations',
                'icon': '🦸',
                'points_required': 50
            },
            {
                'name': 'Champion',
                'description': 'Made 10 blood donations',
                'icon': '🏆',
                'points_required': 100
            },
            {
                'name': 'Legend',
                'description': 'Made 25 blood donations',
                'icon': '👑',
                'points_required': 250
            },
            {
                'name': 'Guardian Angel',
                'description': 'Saved 5 lives',
                'icon': '👼',
                'points_required': 100
            }
        ]

        for achievement_data in achievements:
            Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created achievements'))