import telebot.apihelper
from telebot import TeleBot, types

from . import start_buttons
from helpers.variables import MESSAGES
from helpers import admins, users
from helpers.api import TGUserAPI


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start_handler(message: types.Message):
        if message.chat.type == 'private':
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            start(bot, message.from_user)


def start(bot: TeleBot, user: types.User):
    admin = admins.is_admin(user)
    if admin:
        handle_admin(user, admin)

    tg_user = TGUserAPI.get_tg_user(user.id)

    if tg_user is None:
        users.USERS_CITY_INPUT[user.id] = True

        greeting = f"{MESSAGES['user']['greeting'].format(user.first_name)}\n"  # if not admin else ''

        bot.send_message(
            user.id,
            greeting + MESSAGES['user']['city_not_set']
        )
        return

    # удаление ранее отправленных билетов
    delete_sended_tickets(bot, tg_user)

    # обновление активности пользователя в бд
    tg_user: dict = TGUserAPI.update_tg_user(tg_user)

    # получение кол-ва билетов из города пользователя
    tickets_count: int = 0
    if tg_user and tg_user['city']:
        tickets_count = users.tickets_count(tg_user['city'])

    if tickets_count == 0:
        bot.send_message(
            chat_id=user.id,
            text=MESSAGES['user']['no_tickets_in_city'].format(tg_user['city'].upper())
        )
        return

    bot.send_message(
        user.id,
        MESSAGES['user']['start'].format(
            user.first_name,
            tg_user['city'],
            str(tickets_count)
        ),
        reply_markup=start_buttons.get_months_buttons()
    )


def handle_admin(user: types.User, admin: admins.TGAdmin):
    if user.id not in admins.ADMINS:
        admins.ADMINS[user.id] = admin

    admins.ADMINS[user.id].clear_state()


def delete_sended_tickets(bot: TeleBot, tg_user: dict) -> None:
    if not tg_user['msgs2delete']:
        return

    for ticket_msg_id in tg_user['msgs2delete'].split(',')[::-1]:
        try:
            bot.delete_message(tg_user['user_id'], int(ticket_msg_id))
        except telebot.apihelper.ApiException:
            continue

    tg_user['msgs2delete'] = ''
