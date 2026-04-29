from django import forms
from django.db import connection
from .models import PullRequest, PullRequestLine
from apps.pos.models import PurchaseOrder
from django.forms.models import inlineformset_factory


class PullRequestForm(forms.ModelForm):
    purchase_order = forms.ModelChoiceField(
        queryset=PurchaseOrder.objects.filter(status="RECEIVED"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PullRequest
        fields = ['purchase_order']
        widgets = {
            # 'purchase_order': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

class PullRequestLineForm(forms.ModelForm):
    class Meta:
        model = PullRequestLine
        fields = ['inventory_roll', 'requested_yards', 'notes']
        widgets = {
            'inventory_roll': forms.Select(attrs={'class': 'form-select'}),
            'requested_yards': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


PullRequestLineInlineFormSet = inlineformset_factory(
    PullRequest,
    PullRequestLine,
    form=PullRequestLineForm,
    extra=0,
    can_delete=True,
)