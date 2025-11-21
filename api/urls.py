from django.urls import path
from . import views
from django.urls import path
from .views import search_routes_ai

urlpatterns = [
    path("cities", views.list_cities),
    path("routes/search", views.search_routes),
    path("orders", views.create_order),
    path("orders/<int:order_id>/pay", views.pay_order),
    path("tickets/<int:ticket_id>/status", views.ticket_status),
    path("routes-ai/", search_routes_ai, name="routes-ai"),
]
