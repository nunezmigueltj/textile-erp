from django import forms
from .models import PurchaseOrder, PurchaseOrderFabrics
from apps.companies.models import Vendor
from apps.demand.models import Demand
from apps.fabrics.models import FabricColor
from django.forms.widgets import Select


class IssuePurchaseOrderForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.filter(company__is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    demand = forms.ModelChoiceField(
        queryset=Demand.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'demand', 'expected_delivery',]
        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expected_delivery': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class FabricSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value:  # if fabric
            pk = getattr(value, "value", value)
            try:
                fabric = FabricColor.objects.get(pk=pk)
                option['attrs']['data-price'] = fabric.price
            except FabricColor.DoesNotExist:
                pass
        return option
    

class AssignPurchaseOrderFabricsForm(forms.ModelForm):
    fabric = forms.ModelChoiceField(
        queryset=FabricColor.objects.filter(is_active=True),
        widget=FabricSelect(attrs={'class': 'form-select select_fabric', })
    )

    class Meta:
        model = PurchaseOrderFabrics
        fields = ['fabric', 'yards']
        widgets = {
            'yards': forms.NumberInput(attrs={'class': 'form-control', })
        }

