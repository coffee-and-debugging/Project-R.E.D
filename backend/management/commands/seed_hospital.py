from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from hospitals.models import Hospital
from users.models import User

class Command(BaseCommand):
    help = 'Seed database with sample hospitals'

    def handle(self, *args, **options):
        hospitals_data = [
            {
                'name': 'Central Hospital',
                'address': 'Kathmandu, Nepal',
                'contact': '+977-1-4412345',
                'location': Point(85.3240, 27.7172),
                'admin_username': 'central_admin'
            },
            {
                'name': 'Mercy Hospital',
                'address': 'Lalitpur, Nepal',
                'contact': '+977-1-5512345',
                'location': Point(85.3206, 27.6588),
                'admin_username': 'mercy_admin'
            },
            {
                'name': 'Care Hospital',
                'address': 'Bhaktapur, Nepal',
                'contact': '+977-1-6612345',
                'location': Point(85.4298, 27.6710),
                'admin_username': 'care_admin'
            }
        ]

        for hospital_data in hospitals_data:
            admin_user, created = User.objects.get_or_create(
                username=hospital_data['admin_username'],
                defaults={
                    'email': f"{hospital_data['admin_username']}@hospital.com",
                    'blood_group': 'O+',
                    'age': 35,
                    'sex': 'M',
                    'address': hospital_data['address'],
                    'contact': hospital_data['contact'],
                    'is_staff': True,
                    'is_donor': False
                }
            )
            
            if created:
                admin_user.set_password('hospital123')
                admin_user.save()

            hospital, created = Hospital.objects.get_or_create(
                name=hospital_data['name'],
                defaults={
                    'address': hospital_data['address'],
                    'contact': hospital_data['contact'],
                    'location': hospital_data['location'],
                    'admin': admin_user
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded hospitals'))
