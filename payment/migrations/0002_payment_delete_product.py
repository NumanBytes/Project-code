# Generated by Django 4.2 on 2023-07-05 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_arrival_date'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('status', models.CharField(max_length=255, verbose_name='Payment status')),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order')),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
