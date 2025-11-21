# api/gigachat_client.py
from gigachat import GigaChat
from django.conf import settings
import json

def ask_gigachat(prompt: str) -> str:
    """
    Отправляет запрос в GigaChat и возвращает текст ответа.
    """
    if not settings.GIGACHAT_CREDENTIALS:
        raise RuntimeError("GIGACHAT_CREDENTIALS не задан в .env")

    with GigaChat(
        credentials=settings.GIGACHAT_CREDENTIALS,
        scope=settings.GIGACHAT_SCOPE,
        verify_ssl_certs=settings.GIGACHAT_VERIFY_SSL_CERTS,
    ) as giga:
        response = giga.chat(prompt)
    return response.choices[0].message.content


def classify_routes_with_ai(routes, from_city: str, to_city: str, date_str: str):
    """
    routes — список словарей:
    {
        "id": 1,
        "mode": "plane" / "train" / "bus",
        "price_rub": 25000,
        "duration_min": 600,
        "transfers": 0
    }
    Возвращает такой же список, но с полем category и, по возможности, отсортированный.
    """

    prompt = f"""
Ты ИИ-ассистент мультимодального билетного сервиса.

У тебя есть несколько вариантов маршрута из города "{from_city}" в город "{to_city}" на дату {date_str}.
Для каждого маршрута уже известны цена (price_rub) и длительность в минутах (duration_min).

Твоя задача:
1. Для КАЖДОГО маршрута добавить поле "category" со значением:
   - "fast"  — если маршрут один из самых быстрых;
   - "cheap" — если маршрут один из самых дешёвых;
   - "reliable" — если маршрут с малым количеством пересадок и разумной ценой/временем.
2. Вернуть только JSON-массив без поясняющего текста.
3. Каждый элемент массива должен иметь поля:
   id, mode, price_rub, duration_min, transfers, category.

Входные данные (JSON):
{json.dumps(routes, ensure_ascii=False)}
"""

    answer = ask_gigachat(prompt)

    try:
        parsed = json.loads(answer)
        # на всякий случай убеждаемся, что это список
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    # если GigaChat вернул что-то странное — просто добавим category сами
    for r in routes:
        r.setdefault("category", "reliable")
    return routes
