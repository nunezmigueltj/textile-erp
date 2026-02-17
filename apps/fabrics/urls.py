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
from apps.fabrics import views

app_name = "fabrics"
urlpatterns = [
    path('', views.fabrics_list, name="fabrics_list"),
    path('add/', views.add_fabric, name='add_fabric'),
    path('edit/<int:fabric_id>/', views.edit_fabric, name='edit_fabric'),
    path('deactivate/<int:fabric_id>/', views.deactivate_fabric, name='deactivate_fabric'),
    path('activate/<int:fabric_id>/', views.activate_fabric, name='activate_fabric'),
]
