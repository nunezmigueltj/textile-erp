from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator

User = get_user_model()

# Create your views here.
def users_list(request):
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)
    print(rows_per_page)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE


    users = User.objects.all().order_by('email')

    if q:
        q=q.strip()
        users = users.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q)
            ).order_by('email')

        
    paginator = Paginator(users, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/home.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page})

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


class AddNewSuperUser(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/add_superuser.html"
    success_url = reverse_lazy("users:users_list")


class EditSuperUser(UpdateView):
    model = User
    form_class = RegisterForm
    template_name = "users/edit_superuser.html"
    success_url = reverse_lazy("users:users_list")


def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.is_active = False
        user.save()
        return redirect("users:users_list")
    return render(request, "users/confirm_deactivate.html", {"user": user})


def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.is_active = True
        user.save()
        return redirect("users:users_list")
    return render(request, "users/confirm_activate.html", {"user": user})
        
