# Generated by Django 4.1.5 on 2023-01-29 04:54

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='scheduledevent',
            index=django.contrib.postgres.indexes.GinIndex(fields=['date', 'time'], name='messaging_s_date_659882_gin'),
        ),
        migrations.AddIndex(
            model_name='scheduledevent',
            index=django.contrib.postgres.indexes.GinIndex(fields=['stop_at'], name='messaging_s_stop_at_948632_gin'),
        ),
    ]
