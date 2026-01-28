from django import forms
from .models import Company, Vendor, Customer

class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
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