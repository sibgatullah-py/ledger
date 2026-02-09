from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='entries')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    entry_date = models.DateField()

    def __str__(self):
        return f"{self.customer.name} - {self.type} - {self.amount}"

