from django import forms
from .models import Product, BorrowRequest

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'image', 'made_in', 'material', 'available']
        widgets = {
            'available': forms.CheckboxInput(),
        }

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['first_name', 'last_name', 'take_time', 'bring_time']
        widgets = {
            'take_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'bring_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }