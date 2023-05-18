from telebot import TeleBot, types

from helpers import tg
from helpers.variables import MESSAGES


def handle(bot: TeleBot):
    @bot.message_handler(commands=["city"])
    def city(message: types.Message):
        if message.chat.type != 'private':
            return

        tg.USERS_CITY_INPUT[message.from_user.id] = True
        bot.send_message(
            message.chat.id,
            MESSAGES['user']['city_not_set'].format(message.from_user.first_name)
        )
