from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddColorForm
from .models import Color
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

# Create your views here.
@never_cache
@login_required
def colors_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    active_colors = Color.objects.filter(is_active=True).order_by('name')
    inactive_colors = Color.objects.filter(is_active=False).order_by('name')

    if q:
        q=q.strip()
        active_colors = active_colors.filter(
                Q(code__icontains=q) |
                Q(name__icontains=q) |
                Q(hex_value__icontains=q)
            ).order_by('name')

        
    paginator = Paginator(active_colors, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'colors/home.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page,
                                                 'inactive_colors': inactive_colors})


class AddColorView(CreateView):
    model = Color
    # fields = ['name', 'code', 'hex_value']
    form_class = AddColorForm
    success_url = "/colors/"
    template_name = "colors/add_color.html"


class EditColorView(UpdateView):
    model = Color
    form_class = AddColorForm
    success_url = "/colors/"
    template_name = "colors/edit_color.html"


def deactivate_color(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    if request.method == 'POST':
        color.is_active = False
        color.save()
        return redirect('colors:colors_list')
    return render(request, 'colors/confirm_deactivate.html', {'color': color})


def activate_color(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    if request.method == 'POST':
        color.is_active = True
        color.save()
        return redirect('colors:colors_list')
    return render(request, 'colors/confirm_activate.html', {'color': color})
