from telebot import TeleBot, types

from helpers.variables import MESSAGES
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['photo'])
    def photo(message: types.Message):
        if message.chat.type != 'private':
            return

        if not tg.is_admin(message.from_user):
            bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES['user']['text']
            )
            return

        tg.TGAdmin.add_ticket(bot, message)
