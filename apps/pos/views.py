from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import IssuePurchaseOrderForm, AssignPurchaseOrderFabricsForm
from .models import PurchaseOrder, PurchaseOrderFabrics

# Create your views here.
def pos_list(request):
    return render(request, "pos/pos_list.html", {})


def issue_po(request):
    po_form = IssuePurchaseOrderForm(request.POST or None)
    assign_fabric_form = AssignPurchaseOrderFabricsForm(request.POST or None)
    if request.method == "POST":
        if po_form.is_valid():
            po = po_form.save(commit=False)
    print(request)
    return render(request, "pos/issue_po.html", {"form": po_form, "fabric_form":assign_fabric_form})
