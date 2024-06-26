# Generated by Django 4.2.10 on 2024-04-09 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Cloths',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=256)),
                ('Seller', models.CharField(max_length=256)),
                ('Code', models.CharField(max_length=5)),
                ('MRP', models.IntegerField()),
                ('Date', models.DateField()),
                ('SIZE', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL'), ('3XL', '3XL'), ('4XL', '4XL'), ('5XL', '5XL'), ('6XL', '6XL')], default='S', max_length=3)),
                ('FinalCode', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=256)),
                ('Age', models.IntegerField(default=23)),
                ('PhoneNumber', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=256)),
                ('Seller', models.CharField(max_length=256)),
                ('Code', models.CharField(max_length=5)),
                ('MRP', models.IntegerField()),
                ('Date', models.DateField()),
                ('FinalCode', models.CharField(max_length=256)),
                ('SIZE', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL'), ('3XL', '3XL'), ('4XL', '4XL'), ('5XL', '5XL'), ('6XL', '6XL')], default='S', max_length=3)),
                ('sold_on', models.DateField()),
                ('PhoneNumber', models.CharField(default='0000000000', max_length=10)),
            ],
        ),
    ]
