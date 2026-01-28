from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCompanyForm, AddVendorForm, AddCustomerForm
from .models import Company, Vendor, Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required
def companies_list(request):
    all_companies = Company.objects.all()
    return render(request, 'companies/home.html', {'companies': all_companies})

def add_company(request):
    if request.method == "POST":
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            #
            company.save()
            return redirect('companies:choose_company_role', company_id=company.id)
    else:
        form = AddCompanyForm()
    return render(request, 'companies/add_company.html', {'form': form})

def choose_company_role(request, company_id):
    print(company_id)
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'companies/choose_company_role.html', {"company": company})

def add_vendor(request, company_id):
    company = get_object_or_404(Company, id= company_id)
    if request.method == 'POST':
        form = AddVendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.company = company
            vendor.save()
            return redirect("companies:companies_list")
    else:
        form = AddVendorForm()
    return render(request, 'companies/add_vendor.html',{
            'form': form,
            'company': company
        }) 

def add_customer(request, company_id):
    company = get_object_or_404(Company, id= company_id)
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = company
            customer.save()
            return redirect("companies:companies_list")
    else:
        form = AddCustomerForm()
    return render(request, 'companies/add_customer.html',{
            'form': form,
            'company': company
        }) 
