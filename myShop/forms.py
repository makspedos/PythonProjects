from django import forms
from .models import *


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude=['customer_id']

class CheckoutBuyerForm(forms.Form):
    name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    number = forms.IntegerField(required=True)
    address = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta:
        model = Customers
        exclude=['customer_id']

