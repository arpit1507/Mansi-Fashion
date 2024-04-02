from django.contrib import admin
from first_app.models import Cloths,SoldItem,Customer
# Register your models here.
class SoldItemAdmin(admin.ModelAdmin):
    list_display = ['Description', 'Seller', 'Code', 'MRP', 'Date', 'FinalCode', 'SIZE','sold_on', 'PhoneNumber']
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Age', 'PhoneNumber']
class ClothsAdmin(admin.ModelAdmin):
    list_display = ['Description', 'Seller', 'Code', 'MRP', 'Date', 'FinalCode', 'SIZE']

admin.site.register(SoldItem, SoldItemAdmin)
admin.site.register(Customer, CustomerAdmin)

admin.site.register(Cloths,ClothsAdmin)