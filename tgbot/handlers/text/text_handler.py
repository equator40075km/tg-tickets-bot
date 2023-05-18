from telebot import TeleBot, types
from datetime import date

from helpers.variables import MESSAGES, ADMIN_BUTTONS
from helpers import tg
from helpers.api import TGAdminAPI, TicketAPI, TGUserAPI


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['text'])
    def text(message: types.Message):
        if message.chat.type != 'private':
            return

        if tg.is_admin(message):
            if handle_admin_action(bot, message):
                return

        city_input = tg.USERS_CITY_INPUT.get(message.from_user.id)
        if city_input:
            tg_user_data = {
                'user_id': message.from_user.id,
                'city': message.text,
                'last_action': date.today()
            }

            if TGUserAPI.get_tg_user(message.from_user.id):
                tg_user = TGUserAPI.update_tg_user(tg_user_data)
            else:
                tg_user = TGUserAPI.create_tg_user(tg_user_data)

            if tg_user:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES['user']['city_setted'].format(tg_user['city'])
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Не удалось установить город. Попробуйте ещё раз"
                )

            tg.USERS_CITY_INPUT.pop(message.from_user.id)

            if not tg.tickets_exists(tg_user['city']):
                bot.send_message(
                    chat_id=message.chat.id,
                    text=MESSAGES['user']['no_tickets_in_city'].format(tg_user['city'].upper())
                )

            return

        bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES['user']['text'].format(message.from_user.first_name)
        )
        return


def handle_admin_action(bot: TeleBot, message: types.Message) -> bool:
    admin_id: int = message.from_user.id
    admin_btns: dict = MESSAGES['admin']['btns']

    # добавление билета
    if message.text == admin_btns['add_one_ticket']:
        bot.send_message(
            chat_id=admin_id,
            text=MESSAGES['admin']['adding_ticket']
        )
        return True

    # удаление одного билета
    elif message.text == admin_btns['remove_one_ticket']:
        tickets = TicketAPI.get_all_tickets()
        tmp = ''
        for ticket in tickets:
            tmp += f"{ticket['id']}:\t\t<{ticket['date']}, {ticket['title']}>\n"
        if tmp:
            bot.send_message(chat_id=admin_id, text=tmp)
        else:
            bot.send_message(chat_id=admin_id, text='Не найдено ни одного билета')
            return True

        bot.send_message(admin_id, MESSAGES['admin']['removing_ticket'])
        tg.ADMINS[admin_id].set_removing_ticket()
        return True

    # удаление просроченных билетов
    elif message.text == admin_btns['remove_overdue_tickets']:
        count: int = TicketAPI.remove_overdue_tickets()
        if count == 0:
            bot.send_message(admin_id, 'Нет просроченных билетов')
        elif count > 0:
            bot.send_message(admin_id, MESSAGES['admin']['overdue_tickets_removed'].format(count))
        else:
            bot.send_message(admin_id, 'Не удалось удалить просроченные билеты')
        return True

    # назначение нвого админа
    elif message.text == admin_btns['appoint_admin']:
        bot.send_message(admin_id, MESSAGES['admin']['appointment'])
        tg.ADMINS[admin_id].set_appointment()
        return True

    # удаление админа
    elif message.text == admin_btns['remove_admin']:
        tg_admins = TGAdminAPI.get_tg_admins()
        tmp = ''
        for tg_admin in tg_admins:
            tmp += f"{tg_admin['user_id']}: {tg_admin['name']}\n"
        if tmp:
            bot.send_message(admin_id, tmp)
        else:
            bot.send_message(admin_id, "Ошибка: не удалось найти ни одного администратора")
            return True

        bot.send_message(admin_id, MESSAGES['admin']['removing_admin'])
        tg.ADMINS[admin_id].set_removing_admin()
        return True

    # удаление неактивных пользователей из БД сервера
    elif message.text == admin_btns['remove_inactive_users']:
        count: int = TGUserAPI.remove_inactive_users()
        if count == 0:
            bot.send_message(admin_id, 'Нет неактивных пользователей')
        elif count > 0:
            bot.send_message(
                admin_id,
                f'Из БД сервера были удалены неактивные пользователи в количестве {count} шт'
            )
        else:
            bot.send_message(admin_id, 'Не удалось удалить неактивных пользователей')
        return True

    # действие админа
    if tg.ADMINS[admin_id].is_action():
        tg.ADMINS[admin_id].do_action(bot, message)
        return True

    return False
