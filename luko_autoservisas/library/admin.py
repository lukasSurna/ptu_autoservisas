from django.contrib import admin
from . import models


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0


class ServiceOrderLineInline(admin.TabularInline):
    model = models.ServiceOrder
    extra = 0    


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year')
    search_fields = ('brand', 'model', 'year')
    list_filter = ('brand', 'model', 'year')


class CarAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car_model', 'plate', 'vin', 'color')
    search_fields = ('customer', 'car_model__brand', 'plate', 'vin', 'color')
    fieldsets = (
        ('Customer', {'fields': (('customer'),)}),
        ('Car', {'fields': (('car_model','plate', 'vin', 'color'),)}),
    )
    inlines = [ServiceOrderLineInline]


class PartServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'part_service', 'quantity', 'price')
    search_fields = ('order__car__customer', 'part_service__name', 'quantity', 'price')
    list_filter = ("part_service__name",)
    raw_id_fields = ("order", "part_service")
    


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'order_status')
    search_fields = ('car__customer', 'date', 'order_status')
    inlines = [OrderLineInline]

@admin.register(models.PartServiceReview)
class PartServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("partservice", "reviewer", "created_at")
    list_display_links = ("created_at", )

admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.PartService, PartServiceAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
