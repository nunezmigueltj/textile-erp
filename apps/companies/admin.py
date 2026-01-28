from django.contrib import admin
from .models import Company, Vendor, Customer

# Register your models here.
admin.site.register(Company)
admin.site.register(Vendor)
admin.site.register(Customer)