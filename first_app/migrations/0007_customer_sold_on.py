# Generated by Django 4.2.10 on 2024-02-28 06:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0006_customer_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='sold_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
