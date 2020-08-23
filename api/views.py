from collections import defaultdict
from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework.decorators import api_view
from flights.settings import TOP_10_DIRECTIONS, DATE_FORMAT
from django.core.cache import cache
from rest_framework.response import Response
from .service import parse_ticket, validate_ticket, build_validation_url, build_url


@api_view()
def calendar(request):
    response = defaultdict(dict)
    today = datetime.today().date()
    for direction in TOP_10_DIRECTIONS:
        for day in (today + timedelta(n) for n in range(1, 31)):
            date = day.strftime(DATE_FORMAT)
            key = f"{direction[0]}-{direction[1]}{date}"
            cached_data = cache.get(key)
            if "error" not in cached_data:
                url = request.build_absolute_uri(reverse('validate_flight'))
                cached_data['validate'] = f"{url}?fly_from={direction[0]}" \
                                          f"&fly_to={direction[1]}" \
                                          f"&date={date}" \
                                          f"&token={cached_data['token']}"
            response[key] = cached_data

    print(response)
    return Response(response)


@api_view()
def validate_flight(request):
    params = request.GET
    url = build_validation_url(booking_token=params.get('token'), bnum=2, pnum=1, adults=1)
    invalid = validate_ticket(url)

    if invalid:
        from_, to, date = params.get('fly_from'), params.get('fly_to'), params.get('date')
        key = f"{from_}-{to}{date}"
        cache.delete(key)
        ticket_url = build_url(fly_from=from_, fly_to=to, date_from=date, date_to=date)
        ticket = parse_ticket(ticket_url)
        cache.set(key, ticket)
        return Response({"msg": "Дешевый билет был обновлен", "ticket": ticket})
    else:
        return Response({"msg": "Билет доступен"})
