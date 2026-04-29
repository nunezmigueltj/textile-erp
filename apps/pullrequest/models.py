from django.db import models

from apps.pos.models import PurchaseOrder
from apps.inventory.models import InventoryReceiptLine

# Create your models here.
class PullRequest(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="pulls",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default="PENDING")  # Ejemplo: PENDING, APPROVED, REJECTED

    def __str__(self):
        return f"Pull Request for PO {self.purchase_order.id} ({self.created_at})"


class PullRequestLine(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    pull_request = models.ForeignKey(
        PullRequest,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    inventory_roll = models.ForeignKey(
        InventoryReceiptLine,
        on_delete=models.PROTECT,  # Evita eliminar si hay pulls pendientes
        related_name="pull_lines",
    )
    requested_yards = models.DecimalField(
        max_digits=10, decimal_places=2,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING',
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pull_request} • {self.inventory_roll} ({self.requested_yards} yd)"