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
from apps.colors import views

app_name = "colors"
urlpatterns = [
    path('', views.colors_list, name='colors_list'),
    path('add/', views.AddColorView.as_view(), name='add_color'),
    path('edit/<int:pk>', views.EditColorView.as_view(), name='edit_color'),
    path('deactivate/<int:color_id>', views.deactivate_color, name='deactivate_color'),
    path('activate/<int:color_id>', views.activate_color, name='activate_color'),
]
