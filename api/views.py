# api/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .gigachat_client import classify_routes_with_ai
from .models import City, Order, Ticket
from .gars_client import get_routes_from_gars, map_gars_to_unified_routes

@require_GET
def search_routes_ai(request):
    from_city = request.GET.get("from")
    to_city = request.GET.get("to")
    date_str = request.GET.get("date")

    if not from_city or not to_city or not date_str:
        return JsonResponse(
            {"error": "Параметры from, to, date обязательны"},
            status=400,
        )

    # 1) здесь можно вместо захардкоженных данных вытянуть билеты из БД
    #    (Ticket.objects.filter(...))
    routes = [
        {
            "id": 1,
            "mode": "plane",
            "price_rub": 25200,
            "duration_min": 600,
            "transfers": 0,
        },
        {
            "id": 2,
            "mode": "train",
            "price_rub": 18000,
            "duration_min": 1440,
            "transfers": 1,
        },
        {
            "id": 3,
            "mode": "bus",
            "price_rub": 12000,
            "duration_min": 1800,
            "transfers": 2,
        },
    ]

    routes_ai = classify_routes_with_ai(routes, from_city, to_city, date_str)

    return JsonResponse({"routes": routes_ai})
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
    from_code = request.GET.get("from_city")
    to_code = request.GET.get("to_city")
    date = request.GET.get("date")

    if not (from_code and to_code and date):
        return Response(
            {"detail": "Параметры from_city, to_city и date обязательны"},
            status=400,
        )

    from_city = City.objects.filter(code=from_code).first()
    to_city = City.objects.filter(code=to_code).first()

    route = {
        "id": 1,
        "mode": "bus",
        "fromCode": from_code,
        "toCode": to_code,
        "fromName": from_city.name if from_city else from_code,
        "toName": to_city.name if to_city else to_code,
        "duration": "1H 45M",
        "price": 25020,
        "carrier": "Test carrier",
        "segments": [],
    }

    return Response({"routes": [route]})


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
