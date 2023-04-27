from telebot import TeleBot

from . import help_buttons
from helpers.jsons_loader import load_messages


def handle(bot: TeleBot):
    @bot.message_handler(commands=["help"])
    def help(message):
        if message.chat.type != 'private':
            return

        messages = load_messages()
        if messages is None:
            print('Start handler: msgs is None')
            return

        bot.send_message(
            message.chat.id,
            messages['help'],
            reply_markup=help_buttons.confirm_send
        )
