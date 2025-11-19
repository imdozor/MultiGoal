# api/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import City, Order, Ticket
from .gars_client import get_routes_from_gars, map_gars_to_unified_routes


@api_view(["GET"])
def list_cities(request):
    """
    GET /api/cities
    Возвращает список городов для выпадающих списков на фронте.
    """
    cities = City.objects.all().order_by("name")
    data = [{"id": c.id, "name": c.name, "code": c.code} for c in cities]
    return Response(data)


@api_view(["GET"])
def search_routes(request):
    """
    GET /api/routes/search?from_city=&to_city=&date=
    Поиск маршрутов (пока демо, данные берутся из GARS/заглушки).
    """
    from_city = request.GET.get("from_city")
    to_city = request.GET.get("to_city")
    date = request.GET.get("date")

    if not (from_city and to_city and date):
        return Response(
            {"detail": "Параметры from_city, to_city и date обязательны"},
            status=400,
        )

    gars_rows = get_routes_from_gars(date_from=date, date_to=date)
    routes = map_gars_to_unified_routes(gars_rows)

    return Response({"routes": routes})


@api_view(["POST"])
def create_order(request):
    """
    POST /api/orders
    {
      "route_id": 1,
      "passenger_name": "Иван Иванов"
    }
    """
    route_id = request.data.get("route_id")
    passenger_name = request.data.get("passenger_name")

    if not route_id or not passenger_name:
        return Response(
            {"detail": "Поля route_id и passenger_name обязательны"},
            status=400,
        )

    order = Order.objects.create(
        route_id=route_id,
        passenger_name=passenger_name,
        status="created",
    )

    return Response(
        {
            "id": order.id,
            "route_id": order.route_id,
            "passenger_name": order.passenger_name,
            "status": order.status,
        }
    )


@api_view(["POST"])
def pay_order(request, order_id: int):
    """
    POST /api/orders/{order_id}/pay
    Переводит заказ в статус paid и создаёт билет.
    """
    order = get_object_or_404(Order, id=order_id)
    order.status = "paid"
    order.save(update_fields=["status"])

    ticket = Ticket.objects.create(
        order=order,
        qr_data=f"TICKET:{order.id}",
        status="active",
    )

    return Response(
        {
            "id": ticket.id,
            "order_id": ticket.order_id,
            "qr_data": ticket.qr_data,
            "status": ticket.status,
        }
    )


@api_view(["GET"])
def ticket_status(request, ticket_id: int):
    """
    GET /api/tickets/{ticket_id}/status
    Проверка статуса билета.
    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({"status": "not_found"})

    return Response({"status": ticket.status})
