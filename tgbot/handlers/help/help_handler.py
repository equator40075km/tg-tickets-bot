from telebot import TeleBot, types

from . import help_buttons
from helpers.variables import MESSAGES
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(commands=["help"])
    def help(message: types.Message):
        if message.chat.type != 'private':
            return

        if tg.is_admin(message):
            bot.send_message(
                message.chat.id,
                MESSAGES['help_admin'],
                reply_markup=help_buttons.admin_buttons
            )
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['help'],
            reply_markup=help_buttons.buttons
        )
