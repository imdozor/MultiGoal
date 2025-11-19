import requests

BASE_URL = "https://avibus.gars-ykt.ru:4443/avitest/odata/standard.odata/"
AUTH = ("ХАКАТОН", "123456")


def get_routes_from_gars(date_from: str, date_to: str):
    """
    Упрощённый запрос к OData.
    На хакатоне достаточно просто дернуть реестр актуальных рейсов.
    """
    url = BASE_URL + "InformationRegister_АктуальныеРейсы"
    params = {
        "$format": "json",
    }

    try:
        resp = requests.get(
            url,
            auth=AUTH,
            params=params,
            verify=False,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("value", [])
    except Exception:
        return []


def map_gars_to_unified_routes(rows):
    """
    Перевод сырых данных ГАРС в формат, который ждёт фронтенд.
    Пока просто возвращаем одну демо-запись.
    """
    routes = []

    routes.append(
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
            "date": "23 JAN",
            "baggage": "20 kg",
            "carryOn": "5 kg",
            "quality": "fast",
            "segments": [],
        }
    )

    return routes
