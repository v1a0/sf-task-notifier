# Generated by Django 4.1.5 on 2023-01-29 04:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressee',
            name='operator_code',
            field=models.IntegerField(db_index=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='addressee',
            name='phone_number',
            field=models.BigIntegerField(error_messages={'invalid': 'Invalid phone format. Example: 79998887766'}, unique=True, validators=[django.core.validators.MinValueValidator(70000000000), django.core.validators.MaxValueValidator(79999999999)]),
        ),
    ]
