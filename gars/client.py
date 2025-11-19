import requests

BASE_URL = "https://avibus.gars-ykt.ru:4443/avitest/odata/standard.odata/"
AUTH = ("ХАКАТОН", "123456")  # логин/пароль из инструкции


def get_routes_from_gars(date_from: str, date_to: str):
    """
    Пример запроса к OData:
    берём актуальные рейсы на период [date_from, date_to].
    Формат дат: '2025-01-01'
    """
    url = BASE_URL + "InformationRegister_АктуальныеРейсы"
    params = {
        "$format": "json",
        # TODO: когда разберёшь схему полей в $metadata.xml,
        # добавить сюда правильный $filter по дате/маршруту.
        # Пример:
        # "$filter": (
        #   f"Period ge datetime'{date_from}T00:00:00' "
        #   f"and Period le datetime'{date_to}T23:59:59'"
        # )
    }

    # verify=False, чтобы не ругался на сертификат (на хакатоне это норм)
    resp = requests.get(url, auth=AUTH, params=params, verify=False)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", [])


def map_gars_to_unified_routes(rows):
    """
    Переводим «сырые» данные ГАРС в формат, который ждёт фронтенд.
    Пока заглушка – позже подставишь реальные поля из ответа ГАРС.
    """
    routes = []
    for r in rows:
        routes.append({
            "id": 1,               # потом заменить на r["Ref_Key"] или другое поле
            "mode": "bus",         # тут лучше "bus", т.к. это автобусные рейсы
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
        })
    return routes
