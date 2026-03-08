from urllib.parse import urlencode
from django.utils import timezone


def build_affiliate_url(data: dict) -> str:
    """
    Генерирует ссылку на внешний поиск (пример для Aviasales).
    Важно: Aviasales может иметь свой формат параметров/ссылок — это базовая схема.
    """
    base_url = "https://www.aviasales.ru/search"

    origin = (data.get("origin") or "").strip().upper()
    destination = (data.get("destination") or "").strip().upper()

    depart_date = data.get("depart_date")
    return_date = data.get("return_date")

    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date.isoformat() if depart_date else "",
        "return_date": return_date.isoformat() if return_date else "",
        "adults": int(data.get("adults") or 1),
        "children": int(data.get("children") or 0),
        "cabin": (data.get("cabin") or "ECONOMY"),
    }

    # Уберём пустые параметры, чтобы ссылка была аккуратной
    params = {k: v for k, v in params.items() if v != ""}

    return f"{base_url}?{urlencode(params)}"


def search_offers_stub(data: dict) -> dict:
    """
    Заглушка: возвращает тестовые офферы.
    Не зависит от внешних API.
    """
    origin = (data.get("origin") or "").strip().upper()
    destination = (data.get("destination") or "").strip().upper()
    depart_date = data.get("depart_date")

    depart_str = depart_date.isoformat() if depart_date else timezone.localdate().isoformat()

    return {
        "currency": "RUB",
        "offers": [
            {
                "id": "OF1",
                "price": 18990,
                "airline": "SU",
                "origin": origin,
                "destination": destination,
                "depart_at": f"{depart_str}T08:40",
                "arrive_at": f"{depart_str}T12:15",
                "stops": 0,
                "duration_minutes": 215,
            },
            {
                "id": "OF2",
                "price": 22500,
                "airline": "TK",
                "origin": origin,
                "destination": destination,
                "depart_at": f"{depart_str}T13:10",
                "arrive_at": f"{depart_str}T18:05",
                "stops": 1,
                "duration_minutes": 295,
            },
        ],
        "generated_at": timezone.now().isoformat(),
    }