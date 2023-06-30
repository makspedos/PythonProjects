import re

from django import forms
from .models import *

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude=['customer_id']

class CheckoutBuyerForm(forms.Form):
    delivery_list = [('Відділення "Нова почта"', 'Відділення "Нова почта"'), ("Кур`єр", "Кур`єр")]
    payment_list = [('Готівка', 'Готівка'), ('Кредитна карта', 'Кредитна карта')]

    name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    email = forms.CharField(required=True)
    payment_type = forms.ChoiceField(choices=payment_list, required=True)
    delivery_type = forms.ChoiceField(choices=delivery_list, required=True)
    delivery_list = [('Відділення "Нова почта"', 'Відділення "Нова почта"'), ("Кур`єр", "Кур`єр")]
    payment_list = [('Готівка', 'Готівка'), ('Кредитна карта', 'Кредитна карта')]

    class Meta:
        model = Customers
        exclude=['customer_id']


class ProductFilterForm(forms.Form):
    category = ProductCategory.objects.all()
    brands = Brand.objects.all()
    list_categories = [('', 'Всі категорії')]
    list_brands = [('', 'Всі бренди')]
    for i in brands:
        list_brands.append((i.id, i.brand_name))

    for i in category:
        list_categories.append((i.category_id, i.name))

    list_size = [('','Всі розміри')]
    for i in range(30,45,1):
        list_size.append((i,i))

    product_name = forms.CharField(required=False, label='Назва товару')
    min_price = forms.DecimalField(required=False, label='Мінімальна ціна')
    max_price = forms.DecimalField(required=False, label='Максимальна ціна')
    brand = forms.ChoiceField(choices=list_brands, label='Бренд', widget=forms.RadioSelect, required=False)
    category = forms.ChoiceField(choices=list_categories, label='Категорія', widget=forms.RadioSelect, required=False, )
    size = forms.ChoiceField(choices=list_size, label='Розміри', required=False, )
