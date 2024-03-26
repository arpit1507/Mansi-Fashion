from typing import Any
from django import forms
from first_app.models import Cloths,Customer,AppUser

class AppUser(forms.ModelForm):
    class Meta:
        model = AppUser
        fields='__all__'
        widgets = {
        'password': forms.PasswordInput(),
        }

class Price(forms.ModelForm):
    class Meta():
        model=Cloths
        fields='__all__'

class Customer(forms.ModelForm):
    class Meta():
        model=Customer
        fields='__all__'
    
