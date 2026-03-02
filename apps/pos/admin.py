from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderFabrics

# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderFabrics)