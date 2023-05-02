from telebot import types
from typing import Union, Dict

from . import api


# класс, описывающий админа
class TGAdmin:
    def __init__(self, user_id: int, name: str, can_appoint: bool):
        self.user_id: int = user_id
        self.name: str = name
        self.can_appoint: bool = can_appoint
        self.adding_ticket: bool = False
        self.removing_ticket: bool = False
        self.appointment: bool = False

    def __str__(self):
        return f'{self.user_id}: {self.name}'

    # обнуление текущего взаимодействия
    def clear_state(self):
        self.adding_ticket = False
        self.removing_ticket = False
        self.appointment = False


# словарь состояния админов (user_id: int -> admin: helpers.tg.TGAdmin)
ADMINS: Dict[int, TGAdmin] = {}


def is_admin(message: types.Message) -> Union[TGAdmin, None]:
    if message.from_user.id in ADMINS:
        return ADMINS.get(message.from_user.id, None)

    admins = api.get_tg_admins()
    if admins:
        for admin in admins['tg_admins']:
            if admin['user_id'] == message.from_user.id:
                return TGAdmin(
                    user_id=message.from_user.id,
                    name=message.from_user.username,
                    can_appoint=admin['can_appoint']
                )

    return None
