# api/admin.py
from django.contrib import admin
from .models import City, Order, Ticket, GarsRawEntity


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "created_at")
    search_fields = ("code", "name")
    list_filter = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "route_id", "passenger_name", "status", "created_at")
    search_fields = ("route_id", "passenger_name")
    list_filter = ("status", "created_at")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "created_at")
    search_fields = ("order__id",)
    list_filter = ("status", "created_at")


@admin.register(GarsRawEntity)
class GarsRawEntityAdmin(admin.ModelAdmin):
    list_display = ("id", "entity_type", "ref_key", "created_at")
    search_fields = ("entity_type", "ref_key")
    list_filter = ("entity_type", "created_at")
