from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory, formset_factory

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from apps.pos.models import PurchaseOrder
from apps.fabrics.models import FabricColor
from .models import InventoryReceipt, InventoryReceiptLine
from .forms import InventoryReceiptForm, InventoryReceiptLineFormSet, InventoryReceiptLineForm


def inventory_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    receivers = InventoryReceipt.objects.select_related('purchase_order', 'created_by').order_by('-received_date')

    if q:
        q=q.strip()
        receivers = receivers.filter(
                Q(purchase_order__po_number__icontains=q) |
                Q(received_date__icontains=q) |
                Q(receipt_number__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__item_code__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__vendor_code__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__cuttable__icontains=q) |
                Q(purchase_order__fabrics__fabric__color__name__icontains=q) |
                Q(purchase_order__fabrics__fabric__color__code__icontains=q) |
                Q(lines__received_yards__icontains=q) | 
                Q(lines__expected_yards__icontains=q)
            ).order_by('id').distinct()

        
    paginator = Paginator(receivers, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page})


def create_receipt_from_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)

    if request.method == 'POST':
        receipt_form = InventoryReceiptForm(request.POST)
        line_formset = InventoryReceiptLineFormSet(request.POST)

        if receipt_form.is_valid() and line_formset.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.purchase_order = po
            receipt.created_by = request.user if request.user.is_authenticated else None
            receipt.save()

            # save lines and assign po_fabric if possible
            po_fabrics = list(po.fabrics.all())
            for i, form in enumerate(line_formset):
                if form.cleaned_data:
                    '''
                        Identificación del problema: 
                        Los formsets de Django incluyen campos internos como DELETE para manejar la eliminación 
                        de filas dinámicas. 
                        Estos campos no deben pasarse al modelo.
                        En el código original, se estaba intentando crear una instancia de InventoryReceiptLine 
                        directamente con form.cleaned_data, lo que incluía el campo DELETE. 
                        Esto causaba un error porque el modelo no tiene un campo DELETE.
                        La solución aplicada: Antes de crear la instancia del modelo, se hace una copia de cleaned_data 
                        y se elimina el campo DELETE (si existe):
                    '''
                    cleaned_data = form.cleaned_data.copy()
                    cleaned_data.pop('DELETE', None)
                    line = InventoryReceiptLine(**cleaned_data)
                    line.receipt = receipt
                    if i < len(po_fabrics):
                        line.po_fabric = po_fabrics[i]
                    line.save()
            po.is_active = False
            po.status = "RECEIVED"
            po.save()

            return redirect('inventory:receipt_detail', receipt_id=receipt.id)

    else:
        # GET: pre-fill the receipt form and line formset based on the PO
        receipt_form = InventoryReceiptForm()

        # Create initial data for line formset based on PO fabrics
        initial_lines = []
        for po_fabric in po.fabrics.all():
            initial_lines.append({
                'fabric': po_fabric.fabric,
                'expected_yards': po_fabric.yards,
                'received_yards': po_fabric.yards, 
                'tolerance_percent': 5,
            })

        line_formset = InventoryReceiptLineFormSet(
            initial=initial_lines,
        )

    context = {
        'po': po,
        'receipt_form': receipt_form,
        'line_formset': line_formset,
    }

    return render(request, 'inventory/create_receipt.html', context)


def create_receipt_free(request):
    if request.method == 'POST':
        receipt_form = InventoryReceiptForm(request.POST)
        line_formset = InventoryReceiptLineFormSet(request.POST)

        if receipt_form.is_valid() and line_formset.is_valid():
            # save receiver
            receipt = receipt_form.save(commit=False)
            receipt.created_by = request.user if request.user.is_authenticated else None
            receipt.save()

            # save receiver fabrics
            for form in line_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    cleaned_data = form.cleaned_data.copy()
                    cleaned_data.pop('DELETE', None)
                    line = InventoryReceiptLine(**cleaned_data)
                    line.receipt = receipt
                    line.expected_yards = cleaned_data['received_yards']
                    line.save()

            return redirect('inventory:receipt_detail', receipt_id=receipt.id)
        
    else:
        receipt_form = InventoryReceiptForm()
        line_formset = formset_factory(
            InventoryReceiptLineForm,
            extra = 1  
        )

    context = {
        'receipt_form': receipt_form,
        'line_formset': line_formset,
        'fabrics': FabricColor.objects.all(),
    }

    return render(request, 'inventory/create_receipt_free.html', context)


def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(InventoryReceipt, id=receipt_id)
    context = {'receipt': receipt}
    return render(request, 'inventory/receipt_detail.html', context)