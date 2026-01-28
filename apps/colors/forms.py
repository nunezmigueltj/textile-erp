from django import forms
from .models import Color

class AddColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name', 'code', 'hex_value']