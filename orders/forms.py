from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        phone = PhoneNumberField()
        fields = ['first_name', 'last_name', 'phone', 'address', 'zipcode', 'order_note']