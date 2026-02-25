from django import forms
from .models import GarmentStyle


class AddGarmentForm(forms.ModelForm):
    class Meta:
        model = GarmentStyle
        fields = ['name', 'description', 'fabrics']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'fabrics': forms.SelectMultiple(attrs={'class': 'form-control'}),  # o forms.SelectMultiple
        }