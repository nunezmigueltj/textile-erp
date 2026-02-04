from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCompanyForm, AddVendorForm, AddCustomerForm
from .models import Company, Vendor, Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q


# Create your views here.
@never_cache
@login_required
def companies_list(request):
    # Get vendor and customer company IDs
    vendor_ids = Vendor.objects.values_list('company_id', flat=True)
    customer_ids = Customer.objects.values_list('company_id', flat=True)

    # Get companies not assigned as vendor or customer
    unassigned = Company.objects.exclude(
        Q(id__in=vendor_ids) | Q(id__in=customer_ids)
    )

    # Get full vendor and customer objects (for display)
    vendors = Vendor.objects.select_related('company')
    customers = Customer.objects.select_related('company')

    return render(request, 'companies/home.html', {
            'unassigned': unassigned,
            'vendors': vendors,
            'customers': customers
        })


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


def edit_company_vendor(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    vendor = get_object_or_404(Vendor, company=company)

    company_form = AddCompanyForm(request.POST or None, instance=company)
    vendor_form = AddVendorForm(request.POST or None, instance=vendor)

    if request.method == "POST":
        if company_form.is_valid() and vendor_form.is_valid():
            company_form.save()
            vendor_form.save()
            return redirect('companies:companies_list')

    return render(request, 'companies/edit_company_vendor.html', {
        'company_form': company_form,
        'vendor_form': vendor_form,
        'company': company,
        'vendor': vendor
    })


def edit_company_customer(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    customer = get_object_or_404(Customer, company=company)

    company_form = AddCompanyForm(request.POST or None, instance=company)
    customer_form = AddCustomerForm(request.POST or None, instance=customer)

    if request.method == "POST":
        if company_form.is_valid() and customer_form.is_valid():
            company_form.save()
            customer_form.save()
            return redirect('companies:companies_list')

    return render(request, 'companies/edit_company_customer.html', {
        'company_form': company_form,
        'customer_form': customer_form,
        'company': company,
        'customer': customer
    })


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
