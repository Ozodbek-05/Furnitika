from django import forms
from apps.orders.models import OrderModel


class ShippingForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['city', 'district', 'street', 'home_number', 'additional_info']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your district'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your street'}),
            'home_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your home number'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special delivery instructions'}),
        }
