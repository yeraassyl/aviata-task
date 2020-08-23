from celery import shared_task
from datetime import datetime, timedelta
from django.core.cache import cache
from flights.settings import DATE_FORMAT, TOP_10_DIRECTIONS
from api.service import parse_ticket, build_url

# BY DIRECTION
@shared_task
def cache_flights():
    today = datetime.today().date()

    for fly_from, fly_to in TOP_10_DIRECTIONS:
        for day in (today + timedelta(n) for n in range(1, 31)):
            date = day.strftime(DATE_FORMAT)
            url = build_url(fly_from=fly_from, fly_to=fly_to, date_from=date, date_to=date)
            data = parse_ticket(url)
            cache.set(f"{fly_from}-{fly_to}{date}", data)
