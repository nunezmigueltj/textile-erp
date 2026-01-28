from django.shortcuts import render, redirect
from .models import Fabric
from .forms import AddFabricForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required
def fabrics_list(request):
    fabrics = Fabric.objects.all()
    return render(request, 'fabrics/home.html', {'fabrics': fabrics})

def add_fabric(request):
    if request.method == 'POST':
        form = AddFabricForm(request.POST)
        if form.is_valid():
            fabric = form.save(commit=False)
            # fabric.created_by = request.user
            fabric.save()
            return redirect('fabrics:fabrics_list')
    else:
        form = AddFabricForm()
    return render(request, 'fabrics/add_fabric.html', {'form': form})