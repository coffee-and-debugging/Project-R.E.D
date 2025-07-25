# Generated by Django 5.2.4 on 2025-07-24 11:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=100)),
                ('points_required', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DonationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(max_length=3)),
                ('amount_ml', models.PositiveIntegerField()),
                ('hospital_name', models.CharField(max_length=255)),
                ('patient_saved', models.BooleanField(default=False)),
                ('donation_date', models.DateTimeField(auto_now_add=True)),
                ('points_earned', models.PositiveIntegerField(default=10)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_donations', models.PositiveIntegerField(default=0)),
                ('total_points', models.PositiveIntegerField(default=0)),
                ('lives_saved', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-total_points', '-total_donations'],
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'achievement')},
            },
        ),
    ]
