from django import forms
from .models import Company, Vendor, Customer

class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'street', 'city', 'state', 'zipcode', 'country', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'company@example.com'}),
        }

        # option 1
        # error_messages = {
        #     'name': {
        #         'unique': "The customer name already exists."
        #     }
        # }
        
    # option 2
    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if Company.objects.filter(name=name).exists():
    #         raise forms.ValidationError("A company with this name already exists.")
    #     return name


class AddVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['payment_terms']

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['credit_limit']