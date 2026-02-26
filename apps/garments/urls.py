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
from apps.garments import views

app_name = "garments"
urlpatterns = [
    path('', views.garments_list, name="garments_list"),
    path('add/', views.AddGarmentStyle.as_view(), name="add_garment"),
    path('edit/<int:pk>/', views.EditGarmentStyle.as_view(), name="edit_garment"),
    path('activate/<int:garment_id>/', views.activate_garment, name="activate_garment"),
    path('deactivate/<int:garment_id>/', views.deactivate_garment, name="deactivate_garment"),
]
