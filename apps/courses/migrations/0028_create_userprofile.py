# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0027_update_default_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_start', models.DateTimeField(blank=True, null=True)),
                ('subscription_end', models.DateTimeField(blank=True, null=True)),
                ('total_cases_completed', models.IntegerField(default=0)),
                ('total_correct_observations', models.IntegerField(default=0)),
                ('total_observations', models.IntegerField(default=0)),
                ('total_correct_diagnoses', models.IntegerField(default=0)),
                ('total_diagnoses', models.IntegerField(default=0)),
                ('average_attempts_per_case', models.FloatField(default=0)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'courses_userprofile',
            },
        ),
    ]

