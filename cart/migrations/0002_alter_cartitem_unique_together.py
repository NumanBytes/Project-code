# Generated by Django 4.2 on 2023-07-05 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_options'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
