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
from django.contrib import admin
from django.urls import path
from apps.inventory import views

app_name = "inventory"
urlpatterns = [
    path('', views.inventory_list, name="inventory_list"),
    path('receipt/create/free/', views.create_receipt_free, name="create_receipt_free"),
    path('receipt/create/<int:po_id>/', views.create_receipt_from_po, name="create_receipt_from_po"),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name="receipt_detail"),
    path('receipt/<int:receipt_id>/edit/', views.edit_receipt, name="edit_receipt"),
]
