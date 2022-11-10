from django.contrib import admin
from Contracts_api import models


admin.site.register(models.UserProfile)
admin.site.register(models.Contract)
admin.site.register(models.ContractItem)
admin.site.register(models.Hospital)
admin.site.register(models.Warehouse)
admin.site.register(models.Invoice)
admin.site.register(models.InvoiceItem)
