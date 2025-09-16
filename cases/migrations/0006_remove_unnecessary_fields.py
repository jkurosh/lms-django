# Generated manually to remove unnecessary fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_auto_20250911_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='case',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='case',
            name='published_at',
        ),
    ]
