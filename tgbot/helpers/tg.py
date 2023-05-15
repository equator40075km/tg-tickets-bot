from telebot import types, TeleBot
from typing import Union, Dict

from .api import TicketAPI, TGAdminAPI, TGUserAPI
from .variables import MESSAGES


# класс, описывающий админа
class TGAdmin:
    def __init__(self, user_id: int, name: str, can_appoint: bool):
        self.user_id: int = user_id
        self.name: str = name
        self.can_appoint: bool = can_appoint
        self.adding_ticket: bool = False
        self.removing_ticket: bool = False
        self.appointment: bool = False
        self.removing_admin: bool = False

    def __str__(self):
        return f'{self.user_id}: {self.name}'

    def set_adding_ticket(self):
        self.clear_state()
        self.adding_ticket = True

    def set_removing_ticket(self):
        self.clear_state()
        self.removing_ticket = True

    def set_appointment(self):
        self.clear_state()
        self.appointment = True

    def set_removing_admin(self):
        self.clear_state()
        self.removing_admin = True

    # обнуление текущего взаимодействия
    def clear_state(self):
        self.adding_ticket = False
        self.removing_ticket = False
        self.appointment = False
        self.removing_admin = False

    # выполняет ли админ какое-то действие из кнопок
    def is_action(self):
        return self.adding_ticket or self.removing_ticket or self.appointment or self.removing_admin

    def do_action(self, bot: TeleBot, message: types.Message) -> bool:
        if self.adding_ticket:
            try:
                if message.photo is None:
                    fields: list = message.text.split('\n')
                    photo: str = fields[4]
                    text_index: int = 5
                else:
                    fields: list = message.caption.split('\n')
                    photo: str = message.photo[-1].file_id
                    text_index: int = 4

                ticket: dict = TicketAPI.create_ticket({
                    'title': fields[0],
                    'date': fields[1],
                    'city': fields[2],
                    'link': fields[3],
                    'photo': photo,
                    'text': '\n'.join(fields[text_index:])
                })
                bot.send_message(
                    chat_id=self.user_id,
                    text=f"Билет <{ticket['id']}: {ticket['date']} {ticket['title']}> успешно добавлен"
                )
            except Exception as e:
                bot.send_message(self.user_id, f"Ошибка добавления билета:\n{e}")
                return False

        elif self.removing_ticket:
            try:
                if TicketAPI.remove_ticket(int(message.text)):
                    bot.send_message(self.user_id, 'Билет успешно удален')
                else:
                    bot.send_message(self.user_id, 'Ошибка удаления билета')
            except Exception as e:
                bot.send_message(self.user_id, f"Ошибка удаления билета:\n{e}")
                return False

        elif self.appointment:
            try:
                admin_id, admin_name = message.text.split('\n')
                admin: dict = TGAdminAPI.create_tg_admin({
                    'user_id': int(admin_id),
                    'name': admin_name,
                    'can_appoint': False
                })
                if admin:
                    bot.send_message(self.user_id, f"Администратор {admin['name']} успешно добавлен")
                else:
                    bot.send_message(self.user_id, 'Ошибка добавления администратора')
            except Exception as e:
                bot.send_message(self.user_id, f"Ошибка добавления администратора:\n{e}")
                return False

        elif self.removing_admin:
            try:
                tg_admin_id: int = int(message.text)
                if tg_admin_id == self.user_id:
                    bot.send_message(self.user_id, MESSAGES['admin']['self_removing'])
                    self.clear_state()
                    return False

                if TGAdminAPI.remove_tg_admin(tg_admin_id):
                    bot.send_message(self.user_id, f"Администратор ({tg_admin_id}) успешно удален")
                else:
                    bot.send_message(self.user_id, 'Ошибка удаления администратора')
            except Exception as e:
                bot.send_message(self.user_id, f"Ошибка удаления администратора:\n{e}")
                return False

        self.clear_state()
        return True


# словарь состояния админов (user_id: int -> admin: helpers.tg.TGAdmin)
ADMINS: Dict[int, TGAdmin] = {}


def is_admin(message: types.Message) -> Union[TGAdmin, None]:
    if message.from_user.id in ADMINS:
        return ADMINS.get(message.from_user.id, None)

    admins = TGAdminAPI.get_tg_admins()
    if admins:
        for admin in admins:
            if admin['user_id'] == message.from_user.id:
                return TGAdmin(
                    user_id=message.from_user.id,
                    name=message.from_user.username,
                    can_appoint=admin['can_appoint']
                )

    return None


# словарь состояний ввода города (user_id -> bool)
USERS_CITY_INPUT: Dict[int, bool] = {}
