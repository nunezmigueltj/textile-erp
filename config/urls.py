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
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', namespace='home')),
    path('fabrics/', include('apps.fabrics.urls', namespace='fabrics')),
    path('colors/', include('apps.colors.urls', namespace='colors')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('companies/', include('apps.companies.urls', namespace='companies')),
    path('garments/', include('apps.garments.urls', namespace='garments')),
    path('demand/', include('apps.demand.urls', namespace='demand')),
    path('pos/', include('apps.pos.urls', namespace='pos')),
]
