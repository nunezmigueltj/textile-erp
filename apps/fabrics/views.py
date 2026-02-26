from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Fabric, FabricColor
from .forms import AddFabricForm, AddFabricColorForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView



# Create your views here. 
@never_cache
@login_required
def fabrics_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_fabrics = Fabric.objects.filter(is_active=True).order_by('id')
    inactive_fabrics = Fabric.objects.filter(is_active=False)

    if q:
        q=q.strip()
        active_fabrics = active_fabrics.filter(
                Q(item_code__icontains=q) |
                Q(vendor_code__icontains=q) |
                Q(vendor__company__name__icontains=q) |
                Q(fabric_class__icontains=q) |
                Q(content__icontains=q) |
                Q(country_of_origin__icontains=q)
            ).order_by('id')

        
    paginator = Paginator(active_fabrics, rows_per_page)
    page_number = request.GET.get('page')
    print(f"page_number:::{page_number}")
    page_obj = paginator.get_page(page_number)

    return render(request, 'fabrics/home.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'inactive_fabrics': inactive_fabrics})


def add_fabric(request):
    form = AddFabricForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            fabric = form.save(commit=False)
            # fabric.created_by = request.user
            fabric.save()
            return redirect('fabrics:fabrics_list')
    return render(request, 'fabrics/add_fabric.html', {'form': form})


def edit_fabric(request, fabric_id):
    fabric = get_object_or_404(Fabric, id=fabric_id)
    form = AddFabricForm(request.POST or None, instance=fabric)
    if request.method == 'POST':
        if form.is_valid():
            fabric = form.save(commit=False)
            # fabric.created_by = request.user
            fabric.save()
            return redirect('fabrics:fabrics_list')
    return render(request, 'fabrics/edit_fabric.html', {'form': form})


def deactivate_fabric(request, fabric_id):
    fabric = get_object_or_404(Fabric, id=fabric_id)
    if request.method == 'POST':
        fabric.is_active = False
        fabric.save()
        return redirect("fabrics:fabrics_list")
    return render(request, 'fabrics/confirm_deactivate.html', {"fabric": fabric})

def activate_fabric(request, fabric_id):
    fabric = get_object_or_404(Fabric, id=fabric_id)
    if request.method == 'POST':
        fabric.is_active = True
        fabric.save()
        return redirect("fabrics:fabrics_list")
    return render(request, 'fabrics/confirm_activate.html', {"fabric": fabric})


'''
######################
############
##### FabricColors
###
'''
@never_cache
@login_required
def fabriccolors_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_fabrics = FabricColor.objects.filter(is_active=True).order_by('color__name')
    inactive_fabrics = FabricColor.objects.filter(is_active=False)

    if q:
        q=q.strip()
        active_fabrics = active_fabrics.filter(
                Q(fabric__item_code__icontains=q) |
                Q(fabric__vendor_code__icontains=q) |
                Q(fabric__cuttable__icontains=q) |
                Q(color__code__icontains=q) |
                Q(color__name__icontains=q) |
                Q(lab_dip__icontains=q) |
                Q(fabric__content__icontains=q) |
                Q(price__icontains=q)
            ).order_by('fabric__item_code')

        
    paginator = Paginator(active_fabrics, rows_per_page)
    page_number = request.GET.get('page')
    print(f"page_number:::{page_number}")
    page_obj = paginator.get_page(page_number)

    return render(request, 'fabrics/fabriccolors_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'inactive_fabrics': inactive_fabrics})


class AddFabricColor(CreateView):
    model = FabricColor
    form_class = AddFabricColorForm
    template_name = "fabrics/add_fabriccolor.html"
    success_url = reverse_lazy('fabrics:fabriccolors_list')


class EditFabricColor(UpdateView):
    model = FabricColor
    form_class = AddFabricColorForm
    template_name = "fabrics/edit_fabriccolor.html"
    success_url = reverse_lazy('fabrics:fabriccolors_list')


def deactivate_fabriccolor(request, fabriccolor_id):
    fabric = get_object_or_404(FabricColor, id=fabriccolor_id)
    if request.method == 'POST':
        fabric.is_active = False
        fabric.save()
        return redirect("fabrics:fabriccolors_list")
    return render(request, 'fabrics/confirm_deactivate_fabriccolor.html', {"fabric": fabric})


def activate_fabriccolor(request, fabriccolor_id):
    fabric = get_object_or_404(FabricColor, id=fabriccolor_id)
    if request.method == 'POST':
        fabric.is_active = True
        fabric.save()
        return redirect("fabrics:fabriccolors_list")
    return render(request, 'fabrics/confirm_activate_fabriccolor.html', {"fabric": fabric})
