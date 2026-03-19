from django import forms
from .models import PurchaseOrder, PurchaseOrderFabrics
from apps.companies.models import Vendor
from apps.demand.models import Demand
from apps.fabrics.models import FabricColor
from django.forms.widgets import Select
from django.db.models import Q


class IssuePurchaseOrderForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.filter(company__is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    demand = forms.ModelChoiceField(
        queryset=Demand.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'demand', 'expected_delivery',]
        widgets = {
            'po_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}),
            'expected_delivery': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # new object
            next_id = PurchaseOrder.objects.last().id + 1 if PurchaseOrder.objects.exists() else 1
            self.fields['po_number'].initial = f"PO Fab#{next_id}"
            # For new POs, only show active demands
            self.fields['demand'].queryset = Demand.objects.filter(is_active=True)
        else:
            # For editing, include the current demand even if inactive
            if self.instance.demand:
                self.fields['demand'].queryset = Demand.objects.filter(
                    Q(is_active=True) | Q(id=self.instance.demand.id)
                )
            else:
                self.fields['demand'].queryset = Demand.objects.filter(is_active=True)
    

class AssignPurchaseOrderFabricsForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderFabrics
        fields = ['fabric', 'yards']
        widgets = {
            'yards': forms.NumberInput(attrs={'class': 'form-control', }),
            'fabric': forms.Select(attrs={'class': 'form-select select_fabric', })
        }

