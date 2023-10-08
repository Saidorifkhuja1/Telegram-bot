import requests
from typing import Dict
import settings

def _make_response(method: str, url: str, headers: Dict, params: Dict,
                   timeout: int, success: int = 200) -> requests.Response:
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        timeout=timeout
    )
    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def _get_tickets(method: str, url: str, headers: Dict, params: Dict, currency: str,
                  origin: str, destination: str, departure_date: str, return_date: str = '',
                  timeout: int = 5, func=_make_response) -> requests.Response:
    url = f'https://api.travelpayouts.com/v2/prices/latest'
    params = {
        "currency": currency,
        "origin": origin,
        "destination": destination,
        "depart_date": departure_date,
        "return_date": return_date
    }
    headers = {
        "x-access-token" : settings.api_key
    }
    response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)
    return response


class SiteApiInterface:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickets(self, currency: str, origin: str, destination: str,
                    departure_date: str, return_date: str = '', params: Dict = {}, timeout: int = 5) -> requests.Response:
        url = f'https://api.travelpayouts.com/v2/prices/latest'
        headers = {
            "x-access-token": self.api_key
        }
        return _get_tickets(method='GET', url=url, headers=headers, params=params, currency=currency, origin=origin,
                             destination=destination, departure_date=departure_date, return_date=return_date,
                             timeout= timeout)


if __name__ == '__main__':
    _make_response
    _get_tickets
    SiteApiInterface
