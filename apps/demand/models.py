from django.db import models
from apps.garments.models import GarmentStyle
from apps.companies.models import Customer

# Create your models here.
class Demand(models.Model):
    job = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)
    po_ship_date = models.DateField()
    style = models.ForeignKey(GarmentStyle, on_delete=models.CASCADE)
    total_pieces = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.order_number} ({self.style})"
