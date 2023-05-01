from datetime import date
from json import loads
from os import getenv
from typing import Union

import requests


def api_url(path: str) -> str:
    return f"{getenv('SERVER_URL')}/api/{path}"


def get_all_tickets() -> Union[dict, None]:
    tickets: requests.Response = requests.get(api_url('tickets'))
    if not tickets.ok:
        return None
    return loads(tickets.text)


def get_tickets(month: date, since: int, until: int) -> Union[dict, None]:
    tickets: requests.Response = requests.get(
        api_url(f'tickets?year={month.year}&month={month.month}&since={since}&until={until}')
    )
    if not tickets.ok:
        return None
    return loads(tickets.text)


def get_tg_admins() -> Union[dict, None]:
    admins: requests.Response = requests.get(api_url('tg-admins'))
    if not admins.ok:
        return None
    return loads(admins.text)
