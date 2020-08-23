import time
import requests
from flights.settings import BASE_URL, VALIDATION_URL

def build_url(**params):
    query = ""
    for param, value in params.items():
        query += f"&{param}={value}"

    return BASE_URL + query


def build_validation_url(**params):
    query = "&v=2"
    for param, value in params.items():
        query += f"&{param}={value}"

    return VALIDATION_URL + query


def parse_ticket(url):
    response = requests.get(url).json()
    data = response['data']
    if not data:
        return {"error": "No tickets found"}

    ticket = sorted(data, key=lambda x: x['price'])[0]
    return {
        "price": ticket['price'],
        "token": ticket['booking_token']
    }


def validate_ticket(url):
    while True:
        response = requests.get(url).json()
        if response['flights_checked']:
            return response['price_change'] and response['flights_invalid']
        time.sleep(10)
