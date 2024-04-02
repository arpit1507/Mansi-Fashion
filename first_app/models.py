from django.db import models
from django.utils import timezone

YEAR_IN_SCHOOL_CHOICES = (
    ("S", "S"),
    ("M","M"),
    ("L", "L"),
    ("XL","XL"),
    ("2XL","2XL"),
    ("3XL","3XL"),
    ('4XL','4XL'),
    ('5XL','5XL'),
    ('6XL','6XL')
)

class Cloths(models.Model):
    Description=models.CharField(max_length=256)
    Seller=models.CharField(max_length=256)
    Code=models.CharField(max_length=5)
    MRP=models.IntegerField()
    Date=models.DateField()
    SIZE=models.CharField(max_length=3, choices=YEAR_IN_SCHOOL_CHOICES,default="S")
    FinalCode=models.CharField(max_length=8)

class SoldItem(models.Model):
    Description=models.CharField(max_length=256)
    Seller=models.CharField(max_length=256)
    Code=models.CharField(max_length=5)
    MRP=models.IntegerField()
    Date=models.DateField()
    FinalCode=models.CharField(max_length=256)
    SIZE=models.CharField(max_length=3, choices=YEAR_IN_SCHOOL_CHOICES,default="S")
    sold_on = models.DateField()
    PhoneNumber=models.CharField(max_length=10,default="0000000000")

class Customer(models.Model):
    Name=models.CharField(max_length=256)
    Age=models.IntegerField(default=23)
    PhoneNumber=models.CharField(max_length=10,unique=True)

class AppUser(models.Model):
    Name=models.CharField(max_length=256)
    password=models.CharField(max_length=20)
