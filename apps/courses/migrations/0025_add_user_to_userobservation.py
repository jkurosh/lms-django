# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_bookmark'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userobservation',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_observations', to='users.customuser'),
            preserve_default=False,
        ),
    ]
