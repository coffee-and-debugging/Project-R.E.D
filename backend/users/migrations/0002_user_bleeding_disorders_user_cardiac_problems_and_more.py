# Generated by Django 5.2.4 on 2025-07-25 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bleeding_disorders',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='cardiac_problems',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='donated_blood_before',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='ever_tested_hiv_positive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='fcm_token',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='suffers_any_disease',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='takes_medication',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('Male', 'M'), ('Female', 'F'), ('Others', 'O')], max_length=10),
        ),
    ]
