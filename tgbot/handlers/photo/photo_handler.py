from telebot import TeleBot, types

from helpers.variables import MESSAGES
from helpers import admins


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['photo'])
    def photo(message: types.Message):
        if message.chat.type != 'private':
            return

        if not admins.is_admin(message.from_user):
            bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES['user']['text']
            )
            return

        admins.TGAdmin.add_ticket(bot, message)
