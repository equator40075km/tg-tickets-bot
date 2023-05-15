from telebot import TeleBot, types

from helpers.variables import MESSAGES
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['photo'])
    def photo(message: types.Message):
        if message.chat.type != 'private':
            return

        if not tg.is_admin(message):
            bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES['user']['text']
            )
            return

        admin_id: int = message.from_user.id

        if tg.ADMINS[admin_id].adding_ticket:
            tg.ADMINS[admin_id].do_action(bot, message)
            return

        bot.send_message(admin_id, 'чё это')
