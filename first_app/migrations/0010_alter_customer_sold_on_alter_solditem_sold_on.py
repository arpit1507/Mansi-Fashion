# Generated by Django 4.2.10 on 2024-03-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_alter_cloths_finalcode_alter_solditem_finalcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='sold_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='solditem',
            name='sold_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
