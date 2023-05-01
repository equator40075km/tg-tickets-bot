from telebot import TeleBot, types

from . import start_buttons
from handlers.variables import MESSAGES
from helpers import api


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.type != 'private':
            return

        admins = api.get_tg_admins()
        if admins:
            for admin in admins['tg_admins']:
                if admin['user_id'] == message.from_user.id:
                    handle_admin(bot, message)
                    break
            return

        if 'start' not in MESSAGES:
            print('Start handler: MESSAGES["start"] not found')
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['start'].format(message.from_user.first_name),
            reply_markup=start_buttons.get_months_buttons()
        )


def handle_admin(bot: TeleBot, message: types.Message):
    bot.send_message(
        message.chat.id,
        MESSAGES['start_admin'].format(message.from_user.first_name)
    )
