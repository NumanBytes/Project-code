# Generated by Django 4.2 on 2023-07-05 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
