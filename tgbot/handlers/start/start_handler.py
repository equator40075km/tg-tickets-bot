from telebot import TeleBot, types

from . import start_buttons
from helpers.variables import MESSAGES
from helpers import tg
from helpers.api import TGUserAPI


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start_handler(message: types.Message):
        if message.chat.type == 'private':
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            start(bot, message.from_user)


def start(bot: TeleBot, user: types.User):
    admin = tg.is_admin(user)
    if admin:
        handle_admin(bot, user, admin)

    tg_user = TGUserAPI.get_tg_user(user.id)

    if tg_user is None:
        tg.USERS_CITY_INPUT[user.id] = True

        greeting = f"{MESSAGES['user']['greeting'].format(user.first_name)}\n" if not admin else ''

        bot.send_message(
            user.id,
            greeting + MESSAGES['user']['city_not_set']
        )
        return

    # обновление активности пользователя в бд
    tg_user: dict = TGUserAPI.update_tg_user(tg_user)

    if tg_user and tg_user['city'] and not tg.tickets_exists(tg_user.get('city')):
        bot.send_message(
            chat_id=user.id,
            text=MESSAGES['user']['no_tickets_in_city'].format(tg_user['city'].upper())
        )
        return

    bot.send_message(
        user.id,
        MESSAGES['user']['start'].format(user.first_name, tg_user['city']),
        reply_markup=start_buttons.get_months_buttons()
    )


def handle_admin(bot: TeleBot, user: types.User, admin: tg.TGAdmin):
    if user.id not in tg.ADMINS:
        tg.ADMINS[user.id] = admin

    tg.ADMINS[user.id].clear_state()

    bot.send_message(
        user.id,
        MESSAGES['admin']['start'].format(user.first_name),
        reply_markup=start_buttons.get_admin_buttons(tg.ADMINS[user.id])
    )
