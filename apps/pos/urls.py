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
from apps.pos import views

app_name = "pos"
urlpatterns = [
    path('', views.pos_list, name="pos_list"),
    path('issue/', views.issue_po, name="issue_po"),
    path('edit/<int:po_id>/', views.edit_po, name="edit_po"),
    path('reopen/<int:po_id>/', views.activate_po, name="activate_po"),
    path('close/<int:po_id>/', views.deactivate_po, name="deactivate_po"),
    path('get-vendors/<int:demand_id>/', views.get_vendors_for_demand, name="get_vendors_for_demand"),
    path('get-fabrics/<int:demand_id>/<int:vendor_id>/', views.get_fabrics_for_demand_vendor, name="get_fabrics_for_demand_vendor"),
]
