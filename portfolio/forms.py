from django import forms
from .models import Customer, Investment, Stock, Digitalcurrency


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_number', 'name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone',)


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = (
            'customer', 'category', 'description', 'acquired_value', 'acquired_date', 'recent_value',
            'recent_date',)


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('customer', 'symbol', 'name', 'shares', 'purchase_price', 'purchase_date',)

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Digitalcurrency
        fields = ('customer', 'symbol', 'name', 'balance', 'purchase_price', 'purchase_date',)
