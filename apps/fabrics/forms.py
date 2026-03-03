from django import forms
from .models import Fabric, FabricColor
from apps.colors.models import Color

class AddFabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['item_code', 'vendor_code', 'vendor', 'fabric_class', 'content', 'weight', 'country_of_origin', 'open_or_tubular', 'yarn_type', 'yarn_size', 'cuttable']
        widgets = {
            'item_code': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor_code': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'fabric_class': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'country_of_origin': forms.TextInput(attrs={'class': 'form-control'}),
            'open_or_tubular': forms.Select(attrs={'class': 'form-select'}),
            'yarn_type': forms.TextInput(attrs={'class': 'form-control'}),
            'yarn_size': forms.TextInput(attrs={'class': 'form-control'}),
            'cuttable': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'company@example.com'}),
        }


class AddFabricColorForm(forms.ModelForm):
    fabric = forms.ModelChoiceField(
        queryset=Fabric.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FabricColor
        fields = ['fabric', 'color', 'lab_dip', 'price']
        widgets = {
            'lab_dip': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})
        }