# Generated by Django 4.2 on 2023-07-08 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0015_alter_resetpasswordtoken_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 9, 20, 36, 51, 649887, tzinfo=datetime.timezone.utc), max_length=150),
        ),
    ]
