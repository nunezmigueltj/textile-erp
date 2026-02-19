from django.db import models

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
        # return f"Code: {self.code} - Name: {self.name} - Hex #:{self.hex_value} - Created By: {self.created_by} Created Date: {self.created_at}"
        return f"{self.color_name}"
