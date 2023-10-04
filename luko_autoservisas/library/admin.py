from django.contrib import admin
from . import models

admin.site.register(models.CarModel)
admin.site.register(models.Car)
admin.site.register(models.PartService)
admin.site.register(models.ServiceOrder)
admin.site.register(models.OrderLine)
