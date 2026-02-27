from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import AddDemandForm
from .models import Demand
from apps.companies.models import Company, Customer
from apps.garments.models import GarmentStyle
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
@never_cache
@login_required
def demand_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_demand = Demand.objects.filter(is_active=True).order_by('id')
    closed_demand = Demand.objects.filter(is_active=False)

    if q:
        q=q.strip()
        active_demand = active_demand.filter(
                Q(job__icontains=q) |
                Q(customer__company__name__icontains=q) |
                Q(order_number__icontains=q) |
                Q(po_ship_date__icontains=q) |
                Q(style__name__icontains=q) |
                Q(total_pieces__icontains=q)
            ).order_by('id')

        
    paginator = Paginator(active_demand, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'demand/demand_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'closed_demand': closed_demand})

class AddDemand(CreateView):
    model = Demand
    form_class = AddDemandForm
    template_name = 'demand/add_demand.html'
    success_url = reverse_lazy('demand:demand_list')

class EditDemand(UpdateView):
    model = Demand
    form_class = AddDemandForm
    template_name = 'demand/edit_demand.html'
    success_url = reverse_lazy('demand:demand_list')


def activate_demand(request, demand_id):
    demand = get_object_or_404(Demand, id=demand_id)
    if request.method == 'POST':
        demand.is_active = True
        demand.save()
        return redirect("demand:demand_list")
    return render(request, 'demand/confirm_activate.html', {"demand":demand})


def deactivate_demand(request, demand_id):
    demand = get_object_or_404(Demand, id=demand_id)
    if request.method == 'POST':
        demand.is_active = False
        demand.save()
        return redirect("demand:demand_list")
    return render(request, 'demand/confirm_deactivate.html', {"demand":demand})