"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from apps.companies import views

app_name = "companies"
urlpatterns = [
    path('', views.companies_list, name='companies_list'),
    path('add/', views.add_company, name='add_company'),
    path('choose_role/<int:company_id>/', views.choose_company_role, name='choose_company_role'),
    path('add_vendor/<int:company_id>/', views.add_vendor, name='add_vendor'),
    path('edit_vendor/<int:company_id>/', views.edit_company_vendor, name='edit_company_vendor'),
    path('add_customer/<int:company_id>/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:company_id>/', views.edit_company_customer, name='edit_company_customer'),
    path('edit/<int:company_id>/', views.edit_company, name='edit_company'),
    path('assign_company_role/<int:company_id>/', views.assign_company_role, name='assign_company_role'),
    path('deactivate/<int:company_id>/', views.deactivate_company, name='deactivate_company'),
]
