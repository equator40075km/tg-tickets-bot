from telebot import TeleBot, types

from . import start_buttons
from helpers.variables import MESSAGES
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message: types.Message):
        if message.chat.type != 'private':
            return

        _admin = tg.is_admin(message)
        if _admin:
            handle_admin(bot, message, _admin)
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['start'].format(message.from_user.first_name),
            reply_markup=start_buttons.get_months_buttons()
        )


def handle_admin(bot: TeleBot, message: types.Message, admin: tg.TGAdmin):
    if message.from_user.id not in tg.ADMINS:
        tg.ADMINS[message.from_user.id] = admin

    tg.ADMINS[message.from_user.id].clear_state()

    bot.send_message(
        message.chat.id,
        MESSAGES['start_admin'].format(message.from_user.first_name),
        reply_markup=start_buttons.get_admin_buttons(tg.ADMINS[message.from_user.id])
    )
