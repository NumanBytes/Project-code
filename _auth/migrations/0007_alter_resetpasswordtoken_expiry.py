# Generated by Django 4.2 on 2023-06-02 19:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0006_alter_resetpasswordtoken_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 3, 19, 59, 1, 137611, tzinfo=datetime.timezone.utc), max_length=150),
        ),
    ]