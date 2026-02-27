from django import forms
from .models import Demand
from apps.companies.models import Company, Customer
from apps.garments.models import GarmentStyle

class AddDemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ['job','customer','order_number','po_ship_date','style','total_pieces']
        widgets = {
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(choices=Customer.objects.filter(company__is_active=True), attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'po_ship_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'style': forms.Select(choices=GarmentStyle.objects.filter(is_active=True), attrs={'class': 'form-control'}),
            'total_pieces': forms.NumberInput(attrs={'class': 'form-control'}),
        }