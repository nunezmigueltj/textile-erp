from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.fabrics.models import FabricColor
from apps.pos.models import PurchaseOrder, PurchaseOrderFabrics


class InventoryReceipt(models.Model):
    receipt_number = models.CharField(max_length=30, unique=True)
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="receipts",
    )
    received_date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inventory_receipts",
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Receipt {self.receipt_number} ({self.received_date})"


class InventoryReceiptLine(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_OK = "OK"
    STATUS_UNDER = "UNDER"
    STATUS_OVER = "OVER"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_OK, "Ok"),
        (STATUS_UNDER, "Under"),
        (STATUS_OVER, "Over"),
    ]

    receipt = models.ForeignKey(
        InventoryReceipt,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    fabric = models.ForeignKey(FabricColor, on_delete=models.PROTECT)
    po_fabric = models.ForeignKey(
        PurchaseOrderFabrics,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="receipt_lines",
    )

    # Valores esperados (desde el PO) / recibidos
    expected_yards = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    received_yards = models.DecimalField(max_digits=10, decimal_places=2)

    # Tolerancia en porcentaje (por defecto 5%)
    tolerance_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=5
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.receipt} • {self.fabric} ({self.received_yards} yd)"

    @property
    def percent_diff(self):
        """Porcentaje de diferencia entre recibido y esperado (positivo = sobre, negativo = bajo)."""

        if not self.expected_yards:
            return None

        if self.expected_yards == 0:
            return None

        diff = (self.received_yards - self.expected_yards) / self.expected_yards * 100
        return round(diff, 2)

    def compute_status(self):
        """Calcula y devuelve el estado (OK / UNDER / OVER) usando la tolerancia."""

        if self.expected_yards is None:
            return self.STATUS_PENDING

        diff = self.percent_diff
        if diff is None:
            return self.STATUS_PENDING

        if diff < -abs(float(self.tolerance_percent)):
            return self.STATUS_UNDER
        if diff > abs(float(self.tolerance_percent)):
            return self.STATUS_OVER
        return self.STATUS_OK

    def save(self, *args, **kwargs):
        # Si la linea viene de un PO, aprovechar las cantidades esperadas.
        if self.po_fabric and not self.expected_yards:
            self.expected_yards = self.po_fabric.yards

        if self.po_fabric and not self.fabric:
            self.fabric = self.po_fabric.fabric

        # Actualizamos status en base a tolerancia.
        self.status = self.compute_status()

        super().save(*args, **kwargs)
