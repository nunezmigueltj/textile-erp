from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from .forms import AddGarmentForm
from .models import GarmentStyle, GarmentStyleFabricColor
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required
def garments_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_garments = GarmentStyle.objects.filter(is_active=True).order_by('name')
    inactive_garments = GarmentStyle.objects.filter(is_active=False)

    if q:
        q=q.strip()
        active_garments = active_garments.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q)
            ).order_by('name')

        
    paginator = Paginator(active_garments, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'garments/garments_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'inactive_garments': inactive_garments})


class AddGarmentStyle(CreateView):
    model = GarmentStyle
    form_class = AddGarmentForm
    template_name = 'garments/add_garment.html'
    success_url = reverse_lazy("garments:garments_list")


class EditGarmentStyle(UpdateView):
    model = GarmentStyle
    form_class = AddGarmentForm
    template_name = 'garments/edit_garment.html'
    success_url = reverse_lazy("garments:garments_list")


def activate_garment(request, garment_id):
    garment = get_object_or_404(GarmentStyle, id=garment_id)
    if request.method == 'POST':
        garment.is_active = True
        garment.save()
        return redirect("garments:garments_list")
    return render(request, 'garments/confirm_activate.html', {"garment":garment})


def deactivate_garment(request, garment_id):
    garment = get_object_or_404(GarmentStyle, id=garment_id)
    if request.method == 'POST':
        garment.is_active = False
        garment.save()
        return redirect("garments:garments_list")
    return render(request, 'garments/confirm_deactivate.html', {"garment":garment})

