# Generated by Django 4.2.10 on 2024-04-02 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0021_alter_solditem_finalcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solditem',
            name='BillNo',
        ),
    ]