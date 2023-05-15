from telebot import TeleBot, types

from . import start_buttons
from helpers.variables import MESSAGES
from helpers import tg
from helpers.api import TGUserAPI


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message: types.Message):
        if message.chat.type != 'private':
            return

        admin = tg.is_admin(message)
        if admin:
            handle_admin(bot, message, admin)
            return

        tg_user = TGUserAPI.get_tg_user(message.from_user.id)

        if tg_user is None:
            tg.USERS_CITY_INPUT[message.from_user.id] = True
            bot.send_message(
                message.chat.id,
                MESSAGES['user']['city_not_set'].format(message.from_user.first_name)
            )
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['user']['start'].format(message.from_user.first_name, tg_user['city']),
            reply_markup=start_buttons.get_months_buttons()
        )


def handle_admin(bot: TeleBot, message: types.Message, admin: tg.TGAdmin):
    if message.from_user.id not in tg.ADMINS:
        tg.ADMINS[message.from_user.id] = admin

    tg.ADMINS[message.from_user.id].clear_state()

    bot.send_message(
        message.chat.id,
        MESSAGES['admin']['start'].format(message.from_user.first_name),
        reply_markup=start_buttons.get_admin_buttons(tg.ADMINS[message.from_user.id])
    )
