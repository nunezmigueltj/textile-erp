from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import IssuePurchaseOrderForm, AssignPurchaseOrderFabricsForm
from .models import PurchaseOrder, PurchaseOrderFabrics
from apps.fabrics.models import FabricColor
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@never_cache
@login_required
def pos_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_pos = PurchaseOrder.objects.filter(is_active=True).order_by('id')
    inactive_pos = PurchaseOrder.objects.filter(is_active=False).order_by('id')

    if q:
        q=q.strip()
        active_pos = active_pos.filter(
                Q(po_number__icontains=q) |
                Q(order_date__icontains=q) |
                Q(expected_delivery__icontains=q) |
                Q(status__icontains=q) |
                Q(fabrics__fabric__fabric__item_code__icontains=q) |
                Q(fabrics__fabric__fabric__vendor_code__icontains=q) |
                Q(fabrics__fabric__fabric__cuttable__icontains=q) |
                Q(fabrics__fabric__color__name__icontains=q) |
                Q(fabrics__fabric__color__code__icontains=q)
                # - PurchaseOrder.fabrics → PurchaseOrderFabrics
                # - PurchaseOrderFabrics.fabric → FabricColor
                # - FabricColor.fabric → Fabric
                # - Fabric.item_code → the actual field
            ).order_by('id').distinct()

        
    paginator = Paginator(active_pos, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pos/pos_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'inactive_pos': inactive_pos})


def issue_po(request):
    po_form = IssuePurchaseOrderForm(request.POST or None)
    assign_fabric_form = AssignPurchaseOrderFabricsForm(request.POST or None)

    if request.method == "POST":
        if po_form.is_valid() and assign_fabric_form.is_valid():
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
                return redirect("pos:pos_list")
                
    return render(request, "pos/issue_po.html", {
            "form": po_form, 
            "fabric_form":assign_fabric_form
        })


def edit_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    po_fabrics = PurchaseOrderFabrics.objects.filter(purchase_order=po)

    po_form = IssuePurchaseOrderForm(request.POST or None, instance=po)
    fabric_forms = [AssignPurchaseOrderFabricsForm(instance=fabric) for fabric in po_fabrics]

    if request.method == "POST":
        if po_form.is_valid():
            fabrics = request.POST.getlist("fabric")
            yards = request.POST.getlist("yards")

            with transaction.atomic():
                po = po_form.save()

                updated_fabrics_ids = []

                for index, fabric_id in enumerate(fabrics):
                    po_fabric, created = PurchaseOrderFabrics.objects.get_or_create(
                        fabric_id=fabric_id,
                        purchase_order=po,
                        defaults={"yards": yards[index]}
                    )

                    if not created:
                        po_fabric.yards = yards[index]
                        po_fabric.save()
                    updated_fabrics_ids.append(po_fabric.pk)

                # delete
                po_fabrics.exclude(id__in=updated_fabrics_ids).delete()
                return redirect("pos:pos_list")

    return render(request, "pos/edit_po.html", {"po_form": po_form, "fabric_forms": fabric_forms})



def deactivate_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        po.is_active = False
        po.status = "Closed"
        po.save()
        return redirect("pos:pos_list")
    return render(request, 'pos/confirm_deactivate.html', {"po": po})


def activate_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        po.is_active = True
        po.status = "Open"
        po.save()
        return redirect("pos:pos_list")
    return render(request, 'pos/confirm_activate.html', {"po": po})
