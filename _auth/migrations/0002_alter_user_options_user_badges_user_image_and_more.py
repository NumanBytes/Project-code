# Generated by Django 4.2 on 2023-04-16 19:40

import _auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='badges',
            field=models.PositiveIntegerField(default=0, verbose_name='User Badges'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=_auth.models.image_upload, verbose_name='Profile Photo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('Buyer', 'BUYER'), ('Admin', 'ADMIN')], editable=False, max_length=32, verbose_name='Account Type'),
        ),
    ]
