from django import forms
from django.forms import formset_factory
from django.db import connection
from apps.fabrics.models import FabricColor
from .models import InventoryReceipt, InventoryReceiptLine


class InventoryReceiptForm(forms.ModelForm):
    class Meta:
        model = InventoryReceipt
        fields = ['receipt_number', 'received_date', 'notes']
        widgets = {
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'received_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        table_name = InventoryReceipt._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute("SELECT seq FROM sqlite_sequence WHERE name=%s", [table_name])
            row = cursor.fetchone()
        last_id = row[0] if row else 0
        next_id = last_id + 1

        self.fields['receipt_number'].initial = f"RF-{next_id}"

            


class InventoryReceiptLineForm(forms.Form):
    fabric = forms.ModelChoiceField(queryset=FabricColor.objects.all(), widget=forms.Select(attrs={'class':'form-select'}))
    received_yards = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}))
    tolerance_percent = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'step': '0.01'}), initial=5)


# Formset para las líneas de recepción
InventoryReceiptLineFormSet = formset_factory(
    InventoryReceiptLineForm,
    extra = 0,  # Sin extra por defecto
    can_delete=True,
)