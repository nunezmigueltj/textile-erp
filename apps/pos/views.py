from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import IssuePurchaseOrderForm
from .models import PurchaseOrder, PurchaseOrderFabrics
from django.views.generic import CreateView, UpdateView

# Create your views here.
def pos_list(request):
    return render(request, "pos/pos_list.html", {})

class IssuePurchaseOrder(CreateView):
    model = PurchaseOrder
    form_class = IssuePurchaseOrderForm
    template_name = 'pos/issue_po.html'
    success_url = reverse_lazy("pos:pos_list")
