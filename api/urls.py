from django.urls import path
from . import views

urlpatterns = [
    path("cities", views.list_cities),
    path("routes/search", views.search_routes),
    path("orders", views.create_order),
    path("orders/<int:order_id>/pay", views.pay_order),
    path("tickets/<int:ticket_id>/status", views.ticket_status),
]
