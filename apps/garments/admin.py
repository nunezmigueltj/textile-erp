from django.contrib import admin
from .models import GarmentStyle, GarmentStyleFabricColor

# Register your models here.
admin.site.register(GarmentStyle)
admin.site.register(GarmentStyleFabricColor)