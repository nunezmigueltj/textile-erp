from django import forms
from .models import Color

class AddColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name', 'code', 'hex_value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'hex_value': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'})
        }