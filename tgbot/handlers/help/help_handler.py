from handlers.variables import MESSAGES
from telebot import TeleBot

from . import help_buttons


def handle(bot: TeleBot):
    @bot.message_handler(commands=["help"])
    def help(message):
        if message.chat.type != 'private':
            return

        bot.send_message(
            message.chat.id,
            MESSAGES['help'],
            reply_markup=help_buttons.buttons
        )
