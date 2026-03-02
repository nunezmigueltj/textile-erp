from django.db import models
from apps.companies.models import Vendor
from apps.fabrics.models import FabricColor
from apps.demand.models import Demand
from django.utils import timezone


# Create your models here.
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("APPROVED", "Approved"),
        ("RECEIVED", "Received"),
    ]

    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="purchase_orders")
    demand = models.ForeignKey(Demand, on_delete=models.SET_NULL, related_name="purchase_orders", blank=True, null=True
    )
    order_date = models.DateField(default=timezone.now)
    expected_delivery = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"PO {self.po_number}"


# Fabrics ordered in PO
class PurchaseOrderFabrics(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="fabrics")
    fabric = models.ForeignKey(FabricColor, on_delete=models.PROTECT)
    yards = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fabric.name} - {self.yards} yards"
