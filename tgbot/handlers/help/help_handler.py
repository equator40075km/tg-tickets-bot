from telebot import TeleBot, types

from . import help_buttons
from helpers.variables import MESSAGES
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(commands=["help"])
    def help(message: types.Message):
        if message.chat.type != 'private':
            return

        bot.delete_message(chat_id=message.chat.id, message_id=message.id)

        if tg.is_admin(message.from_user):
            bot.send_message(
                message.chat.id,
                MESSAGES['admin']['help'],
                reply_markup=help_buttons.admin_buttons
            )
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['user']['help'],
            reply_markup=help_buttons.buttons
        )
