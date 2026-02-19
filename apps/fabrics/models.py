from django.db import models
from apps.companies.models import Vendor
from apps.colors.models import Color

# Create your models here.
class Fabric(models.Model):
    open_or_tubular = [
        ('open', 'Open'),
        ('tubular', 'Tubular')
    ]
    item_code = models.CharField(max_length=50, unique=True)
    vendor_code = models.CharField(max_length=50)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    fabric_class = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    country_of_origin = models.CharField(max_length=50)
    open_or_tubular = models.CharField(choices=open_or_tubular)
    # optional fields
    yarn_type = models.CharField(max_length=50, blank=True, null=True)
    yarn_size = models.CharField(max_length=50, blank=True, null=True)
    cuttable = models.IntegerField()
    is_active = models.BooleanField(default=True)

    @property
    def item_merged(self):
        return f"{self.item_code}-{self.vendor_code}-{self.cuttable}"

    def __str__(self):
        return f"{self.item_merged}"
    

class FabricColor(models.Model):
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    lab_dip = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fabric', 'color'], name='unique_fabric_color', violation_error_message="This fabric & color is already registered.")
        ]


    def __str__(self):
        return f"{self.fabric.item_merged} - {self.color.color_name}"

