# Generated by Django 4.2 on 2023-07-10 14:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0016_alter_resetpasswordtoken_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 11, 14, 7, 24, 705250, tzinfo=datetime.timezone.utc), max_length=150),
        ),
    ]