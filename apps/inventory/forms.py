from django import forms
from django.db import connection
from .models import InventoryReceipt, InventoryReceiptLine
from django.forms.models import inlineformset_factory


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


class InventoryReceiptLineForm(forms.ModelForm):
    class Meta:
        model = InventoryReceiptLine
        fields = ['fabric', 'received_yards', 'tolerance_percent']
        widgets = {
            'fabric': forms.Select(attrs={'class': 'form-select'}),
            'received_yards': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'tolerance_percent': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }


InventoryReceiptLineInlineFormSet = inlineformset_factory(
    InventoryReceipt,
    InventoryReceiptLine,
    form=InventoryReceiptLineForm,
    extra=0,
    can_delete=True,
)