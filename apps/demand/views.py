from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import AddDemandForm
from .models import Demand
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.db.models import Q
from apps.pos.forms import IssuePurchaseOrderForm, AssignPurchaseOrderFabricsForm
from django.db import transaction
from apps.pos.models import PurchaseOrderFabrics
from apps.fabrics.models import FabricColor

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


def issue_po(request, demand_id):
    demand = Demand.objects.get(id=demand_id)
    # style = demand.style
    fabrics = demand.style.fabrics.all()
    vendors = list({fabric.fabric.vendor for fabric in fabrics}) #unique, set
    po_form = IssuePurchaseOrderForm(request.POST or None)
    fabric_form = AssignPurchaseOrderFabricsForm(request.POST or None)

    if request.method == "POST":
        print(f"request.POST:::{request.POST}")
        if po_form.is_valid():
            print("is valid")
            fabrics = request.POST.getlist("fabric")
            yards = request.POST.getlist("yards")

            with transaction.atomic():
                po = po_form.save(commit=False)
                po.save()

                po_fabrics = []
                for index,fabric in enumerate(fabrics):
                    po_fabrics.append(PurchaseOrderFabrics(
                        purchase_order=po,
                        fabric=get_object_or_404(FabricColor, id=fabric),
                        yards=yards[index]
                    ))
                #bulk create
                PurchaseOrderFabrics.objects.bulk_create(po_fabrics)
                demand.is_active = False
                demand.save()
                return redirect("demand:demand_list")
                
    return render(request, 'demand/issue_po.html', {
        "demand": demand,
        # "style":style, 
        # "fabrics":fabrics, 
        "form": po_form, 
        "fabric_form": fabric_form,
        "vendors": vendors
    })
    

def get_fabrics_for_demand_vendor(request, demand_id, vendor_id):
    demand = Demand.objects.get(pk=demand_id)
    fabrics = demand.style.fabrics.filter(fabric__vendor_id=vendor_id)
    
    data = [{"id": f.id, "name": str(f), "price": f.price, "vendor": f.fabric.vendor.company.name} for f in fabrics]
    return JsonResponse(data, safe=False)