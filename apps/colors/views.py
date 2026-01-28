from django.shortcuts import render, redirect
from .forms import AddColorForm
from .models import Color
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required
def colors_list(request):
    all_colors = Color.objects.all()
    return render(request, 'colors/home.html', {"colors": all_colors})

def add_color(request):
    if request.method == "POST":
        form = AddColorForm(request.POST)
        if form.is_valid():
            color = form.save(commit=False) #instancia creada, pero no se guarda en BD
            #color.created_by = request.user
            color.save()
            return redirect('colors:colors_list') #como incluimos namespace, se debe poner primero 
                                                  #y despues el name de la url
    else:
        form = AddColorForm()
    return render(request, 'colors/add_color.html', {"form": form})