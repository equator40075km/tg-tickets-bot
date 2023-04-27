from telebot import TeleBot

from . import start_buttons
from helpers.jsons_loader import load_messages


def handle(bot: TeleBot):
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.type != 'private':
            return

        messages = load_messages()
        if 'start' not in messages:
            print('Start handler: messages["start"] not found')
            return

        bot.send_message(
            message.chat.id,
            messages['start'].format(message.from_user.first_name),
            reply_markup=start_buttons.get_months_buttons()
        )
