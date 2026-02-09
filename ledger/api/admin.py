from django.contrib import admin
from .models import Customer, LedgerEntry

# registering the models
admin.site.register(Customer)
admin.site.register(LedgerEntry)

