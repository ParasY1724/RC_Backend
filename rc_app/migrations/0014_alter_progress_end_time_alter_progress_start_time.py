# Generated by Django 5.0.1 on 2024-02-04 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rc_app', '0013_progress_prev_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 4, 18, 40, 10, 568963, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 4, 18, 40, 10, 568963, tzinfo=datetime.timezone.utc)),
        ),
    ]
