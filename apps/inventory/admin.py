from django.contrib import admin
from .models import InventoryReceipt, InventoryReceiptLine

admin.site.register(InventoryReceipt)
admin.site.register(InventoryReceiptLine)
