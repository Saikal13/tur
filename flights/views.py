from django.shortcuts import render, redirect
from .forms import FlightSearchForm
from .services import build_affiliate_url, search_offers_stub
from django.utils.dateparse import parse_date



def flights(request):
    form = FlightSearchForm(request.GET or None)
    offers = None
    affiliate_url = None

    if form.is_valid():
        data = form.cleaned_data

        affiliate_url = build_affiliate_url(data)
        offers = search_offers_stub(data)

    return render(request, "flights/flights.html", {
        "form": form,
        "offers": offers,
        "affiliate_url": affiliate_url,
    })


def flights_redirect(request):
    form = FlightSearchForm(request.GET or None)
    if not form.is_valid():
        return redirect("/flights/")

    return redirect(build_affiliate_url(form.cleaned_data))

def ticket_demo(request):
    """
    Демо-билет после "оплаты".
    Данные приходят через GET параметры (потому что демо).
    """
    passenger_name = (request.GET.get("name") or "").strip() or "IVAN IVANOV"
    email = (request.GET.get("email") or "").strip() or "demo@mail.com"

    origin = (request.GET.get("origin") or "SVO").upper()[:3]
    destination = (request.GET.get("destination") or "IST").upper()[:3]

    depart_at = request.GET.get("depart_at") or "2026-03-03T08:40"
    arrive_at = request.GET.get("arrive_at") or "2026-03-03T12:15"

    airline = (request.GET.get("airline") or "SU").upper()[:3]
    stops = int(request.GET.get("stops") or 0)
    price = request.GET.get("price") or "18990"
    currency = request.GET.get("currency") or "RUB"
    cabin = request.GET.get("cabin") or "ECONOMY"

    # Простейшие демо-значения
    flight_no = request.GET.get("flight_no") or f"{airline} {origin}{destination}".upper()
    gate = request.GET.get("gate") or "A12"
    seat = request.GET.get("seat") or "12C"
    pnr = request.GET.get("pnr") or "TP6K9Q"

    context = {
        "passenger_name": passenger_name,
        "email": email,
        "origin": origin,
        "destination": destination,
        "depart_at": depart_at,
        "arrive_at": arrive_at,
        "airline": airline,
        "stops": stops,
        "price": price,
        "currency": currency,
        "cabin": cabin,
        "flight_no": flight_no,
        "gate": gate,
        "seat": seat,
        "pnr": pnr,
    }
    return render(request, "flights/ticket.html", context)