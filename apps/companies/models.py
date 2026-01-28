from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    @property
    def address(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zipcode}, {self.country}"
    
    def __str__(self):
        return f"{self.name} - {self.address}"

class Vendor(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    payment_terms = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company.name} - {self.payment_terms}"

class Customer(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.company.name} - {self.credit_limit}"
