from typing import Dict, List
from datetime import date, datetime, timedelta

from .api import TicketAPI, TGUserAPI


# словарь состояний ввода города пользователей
USERS_CITY_INPUT: Dict[int, bool] = {}


def tickets_count(city: str) -> int:
    future_date: datetime = datetime.today() + timedelta(days=65)
    tickets = TicketAPI.get_tickets(city, date.today(), future_date.date())
    return len(tickets) if tickets else 0


def add_user_msgs_ids(tg_user: dict, msgs_ids: List[int]) -> None:
    if len(msgs_ids) == 0:
        return

    if tg_user['msgs2delete']:
        tg_user['msgs2delete'] += f",{','.join(map(str, msgs_ids))}"
    else:
        tg_user['msgs2delete'] = ','.join(map(str, msgs_ids))

    TGUserAPI.update_tg_user(tg_user)
