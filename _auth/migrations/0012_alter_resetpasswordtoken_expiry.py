# Generated by Django 4.2 on 2023-07-04 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0011_alter_resetpasswordtoken_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 5, 14, 26, 40, 167842, tzinfo=datetime.timezone.utc), max_length=150),
        ),
    ]
