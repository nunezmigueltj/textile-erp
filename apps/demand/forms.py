from django import forms
from .models import Demand
from apps.companies.models import Company, Customer
from apps.garments.models import GarmentStyle

class AddDemandForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(company__is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    style = forms.ModelChoiceField(
        queryset=GarmentStyle.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Demand
        fields = ['job','customer','order_number','po_ship_date','style','total_pieces']
        widgets = {
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'po_ship_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_pieces': forms.NumberInput(attrs={'class': 'form-control'}),
        }