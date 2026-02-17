from django.db import models

# Create your models here.
# class Fabric(models.Model):
#     item_code = models.CharField(max_length=50)
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
#     fabric_class = models.CharField(max_length=50)
#     content = models.CharField(max_length=100)
#     weight = models.DecimalField(max_digits=6, decimal_places=2)
#     country_of_origin = models.CharField(max_length=50)
#     # optional fields
#     yarn_type = models.CharField(max_length=50, blank=True, null=True)
#     yarn_size = models.CharField(max_length=50, blank=True, null=True)
#     cuttable = models.BooleanField(default=True)

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    hex_value = models.CharField(max_length=7, blank=True, null=True)
    created_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # fecha de creación automática
    is_active = models.BooleanField(default=True)

    @property
    def color_name(self):
        return f"{self.code} - {self.name}"
    
    def __str__(self):
        return f"Code: {self.code} - Name: {self.name} - Hex #:{self.hex_value} - Created By: {self.created_by} Created Date: {self.created_at}"


# class FabricColor(models.Model):
#     fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.CASCADE)

# class FabricReceiving(models.Model):
#     fabric_color = models.ForeignKey(FabricColor, on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)
#     unit = models.CharField(max_length=20, choices=[('yards','Yards'),('meters','Meters'),('rolls','Rolls')])
#     date_received = models.DateField()
#     vendor_reference = models.CharField(max_length=100, blank=True, null=True)