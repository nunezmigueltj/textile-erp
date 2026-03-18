from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory, formset_factory

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from apps.pos.models import PurchaseOrder
from apps.fabrics.models import FabricColor
from .models import InventoryReceipt, InventoryReceiptLine
from .forms import InventoryReceiptForm, InventoryReceiptLineForm, InventoryReceiptLineInlineFormSet 


def inventory_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    receivers = InventoryReceipt.objects.select_related('purchase_order', 'created_by').order_by('-id')


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
            ).distinct().order_by('-id')

        
    paginator = Paginator(receivers, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page})


def create_receipt_from_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)

    # how many fabrics are in this PO? It will generate that many line forms
    fabrics_count = po.fabrics.count()

    # extra = fabrics_count means that it will generate as many empty forms as fabrics in the PO
    LineFormSet = inlineformset_factory(
        InventoryReceipt,
        InventoryReceiptLine,
        form=InventoryReceiptLineForm,
        extra=fabrics_count,
        can_delete=True
    )

    if request.method == 'POST':
        receipt_form = InventoryReceiptForm(request.POST)
        line_formset = LineFormSet(request.POST, instance=InventoryReceipt(), prefix='lines')

        if receipt_form.is_valid() and line_formset.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.purchase_order = po
            receipt.save()

            lines = line_formset.save(commit=False)
            po_fabrics = list(po.fabrics.all())
            for i, line in enumerate(lines):
                line.receipt = receipt
                if i < len(po_fabrics):
                    line.po_fabric = po_fabrics[i]
                line.save()
            
            po.is_active = False
            po.status = "RECEIVED"
            po.save()
            
            return redirect('inventory:receipt_detail', receipt_id=receipt.id)
    else:
        receipt_form = InventoryReceiptForm()

        initial_lines = []
        for po_fabric in po.fabrics.all():
            initial_lines.append({
                'fabric': po_fabric.fabric,
                'expected_yards': po_fabric.yards,
                'received_yards': po_fabric.yards,
                'tolerance_percent': 5,
            })

        line_formset = LineFormSet(
            instance=InventoryReceipt(),
            queryset=InventoryReceiptLine.objects.none(),
            initial=initial_lines,
            prefix='lines'
        )

    return render(request, 'inventory/create_receipt.html', {
        'po': po,
        'receipt_form': receipt_form,
        'line_formset': line_formset,
    })


def create_receipt_free(request):
    LineFormSet = inlineformset_factory(
        InventoryReceipt,
        InventoryReceiptLine,
        form=InventoryReceiptLineForm,
        fields=['fabric', 'received_yards'],
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        receipt_form = InventoryReceiptForm(request.POST)

        if receipt_form.is_valid():
            receipt = receipt_form.save(commit=False)
            receipt.created_by = request.user if request.user.is_authenticated else None
            receipt.save()

            # define prefix for the formset to avoid conflicts with other forms on the page
            line_formset = LineFormSet(request.POST, instance=receipt, prefix='lines')

            if line_formset.is_valid():
                lines = line_formset.save(commit=False)
                for line in lines:
                    line.expected_yards = line.received_yards
                    line.save()
                for line in line_formset.deleted_objects:
                    line.delete()

                return redirect('inventory:receipt_detail', receipt_id=receipt.id)
    else:
        receipt_form = InventoryReceiptForm()
        line_formset = LineFormSet(instance=InventoryReceipt(), prefix='lines')

    return render(request, 'inventory/create_receipt_free.html', {
        'receipt_form': receipt_form,
        'line_formset': line_formset,
    })


def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(InventoryReceipt, id=receipt_id)
    context = {'receipt': receipt}
    return render(request, 'inventory/receipt_detail.html', context)


def edit_receipt(request, receipt_id):
    receipt = get_object_or_404(InventoryReceipt, id=receipt_id)

    if request.method == 'POST':
        receipt_form = InventoryReceiptForm(request.POST, instance=receipt)
        line_formset = InventoryReceiptLineInlineFormSet(request.POST, instance=receipt)

        if receipt_form.is_valid() and line_formset.is_valid():
            receipt_form.save()
            line_formset.save()
            return redirect('inventory:receipt_detail', receipt_id=receipt.id)

    else:
        receipt_form = InventoryReceiptForm(instance=receipt)
        line_formset = InventoryReceiptLineInlineFormSet(instance=receipt)

    context = {
        'receipt': receipt,
        'receipt_form': receipt_form,
        'line_formset': line_formset,
        'fabrics': FabricColor.objects.all(),
    }

    return render(request, 'inventory/edit_receipt.html', context)