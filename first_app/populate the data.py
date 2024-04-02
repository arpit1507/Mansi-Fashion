from models import SoldItem,Customer
for item in SoldItem.objects.all():
    try:
        customer = Customer.objects.get(PhoneNumber=item.PhoneNumber)
        item.customer = customer
        item.save()
    except Customer.DoesNotExist:
        # Handle the case where a matching customer doesn't exist
        pass