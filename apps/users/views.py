from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache


# Create your views here.
def users_list(request):
    return render(request, 'users/home.html')

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            next_url = request.GET.get('next') or 'home:home'
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})

# if user is login, i dont want the user to be able to enter this url..
@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # default commit=True, enters forms.py def save()
            # login(request, user) # enter with no login html
            return redirect('users:login_view')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('users:login_view')