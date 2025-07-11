# Generated by Django 5.2.4 on 2025-07-07 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('preferred_name', models.CharField(blank=True, max_length=100, null=True)),
                ('profession', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
