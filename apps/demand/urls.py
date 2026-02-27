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
from apps.demand import views

app_name = "demand"
urlpatterns = [
    path('', views.demand_list, name='demand_list'),
    path('add/', views.AddDemand.as_view(), name='add_demand'),
    path('edit/<int:pk>', views.EditDemand.as_view(), name='edit_demand'),
    path('activate/<int:demand_id>', views.activate_demand, name='activate_demand'),
    path('deactivate/<int:demand_id>', views.deactivate_demand, name='deactivate_demand'),
]
