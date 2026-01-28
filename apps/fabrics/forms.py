from django import forms
from .models import Fabric

class AddFabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = '__all__'