from datetime import date
from json import loads
from os import getenv
from typing import Union

import requests


def api_url(path: str) -> str:
    return f"{getenv('SERVER_URL')}/api/v1/{path}"


class TicketAPI:
    @staticmethod
    def get_all_tickets() -> Union[dict, None]:
        tickets: requests.Response = requests.get(api_url('tickets'))
        if not tickets.ok:
            return None
        return loads(tickets.text)

    @staticmethod
    def get_tickets(city: str, date_since: date, date_until: date) -> Union[dict, None]:
        city = city.upper()
        tickets: requests.Response = requests.get(
            api_url('tickets/'),
            data={
                'city': city,
                'date_since': date_since.isoformat(),
                'date_until': date_until.isoformat()
            }
        )
        if not tickets.ok:
            return None
        return loads(tickets.text)

    @staticmethod
    def create_ticket(ticket: dict) -> Union[dict, None]:
        ticket['city'] = str(ticket['city']).upper()
        ticket: requests.Response = requests.post(
            url=api_url('tickets/'),
            data=ticket
        )
        if not ticket.ok:
            return None
        return loads(ticket.text)

    @staticmethod
    def remove_ticket(ticket_id: int) -> bool:
        ticket: requests.Response = requests.delete(api_url(f'tickets/{ticket_id}'))
        return ticket.ok

    @staticmethod
    def remove_overdue_tickets() -> int:
        response: requests.Response = requests.delete(api_url('tickets/overdue'))
        if not response.ok:
            return -1
        return loads(response.text)['count']


class TGAdminAPI:
    @staticmethod
    def get_tg_admins() -> Union[dict, None]:
        admins: requests.Response = requests.get(api_url('tg-admins'))
        if not admins.ok:
            return None
        return loads(admins.text)

    @staticmethod
    def create_tg_admin(tg_admin: dict) -> Union[dict, None]:
        response: requests.Response = requests.post(
            api_url('tg-admins/'),
            data=tg_admin
        )
        if not response.ok:
            return None
        return loads(response.text)

    @staticmethod
    def remove_tg_admin(user_id: int) -> bool:
        response: requests.Response = requests.delete(api_url(f'tg-admins/{user_id}'))
        return response.ok


class TGUserAPI:
    @staticmethod
    def get_tg_user(user_id: int) -> Union[dict, None]:
        tg_user: requests.Response = requests.get(api_url(f'tg-users/{user_id}'))
        if not tg_user.ok:
            return None
        return loads(tg_user.text)

    @staticmethod
    def create_tg_user(tg_user: dict) -> Union[dict, None]:
        tg_user['city'] = str(tg_user['city']).upper()
        response: requests.Response = requests.post(
            api_url(f'tg-users/'),
            data=tg_user
        )
        if not response.ok:
            return None
        return loads(response.text)

    @staticmethod
    def update_tg_user(tg_user: dict) -> Union[dict, None]:
        try:
            tg_user['city'] = str(tg_user['city']).upper()
            response: requests.Response = requests.put(
                api_url(f"tg-users/{tg_user['user_id']}/"),
                data=tg_user
            )
            if not response.ok:
                return None
            return loads(response.text)
        except KeyError:
            return None

    @staticmethod
    def remove_inactive_users() -> int:
        response: requests.Response = requests.delete(api_url('tg-users/inactive'))
        if not response.ok:
            return -1
        return loads(response.text)['count']
