from django.db import models
from apps.fabrics.models import FabricColor

# Create your models here.
class GarmentStyle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    fabrics = models.ManyToManyField(FabricColor, through="GarmentStyleFabricColor")

    def __str__(self):
        return self.name

class GarmentStyleFabricColor(models.Model):
    garment_style = models.ForeignKey(GarmentStyle, on_delete=models.CASCADE)
    fabriccolor = models.ForeignKey(FabricColor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("garment_style", "fabriccolor")

    def __str__(self):
        return f"{self.garment_style.name} - {self.fabriccolor}"