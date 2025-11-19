from django.shortcuts import render
from django.http import JsonResponse
from .client import get_routes_from_gars, map_gars_to_unified_routes


def search_routes(request):
    """
    /api/routes/search?from_city=Yakutsk&to_city=Dawtests&date=2025-01-01
    """
    from_city = request.GET.get("from_city")
    to_city = request.GET.get("to_city")
    date = request.GET.get("date")

    if not (from_city and to_city and date):
        return JsonResponse(
            {"error": "Нужно передать from_city, to_city и date"},
            status=400,
        )

    try:
        rows = get_routes_from_gars(date, date)
        routes = map_gars_to_unified_routes(rows)
    except Exception as e:
        # на хакатоне можно просто вернуть заглушку, как в FastAPI
        routes = [
            {
                "id": 1,
                "mode": "bus",
                "fromCode": "YKS",
                "toCode": "DWS",
                "duration": "1H 45M",
                "price": 25020,
                "depTime": "18:20",
                "arrTime": "20:05",
                "depCity": "Yakutsk",
                "arrCity": "Dawtests",
                "date": date,
                "baggage": "20 kg",
                "carryOn": "5 kg",
                "error": str(e),
            }
        ]

    return JsonResponse(
        {
            "from": from_city,
            "to": to_city,
            "routes": routes,
        },
        json_dumps_params={"ensure_ascii": False},
    )
