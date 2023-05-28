from telebot import TeleBot, types

from helpers import admins
from helpers.variables import MESSAGES
from . import admin_buttons
from helpers.api import TicketAPI


def handle(bot: TeleBot):
    @bot.message_handler(commands=["admin"])
    def city(message: types.Message):
        if message.chat.type != 'private':
            return

        admin = admins.is_admin(message.from_user)
        if admin is None:
            return

        all_tickets = TicketAPI.get_all_tickets()

        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            bot.send_message(
                message.from_user.id,
                MESSAGES['admin']['start'].format(
                    str(len(all_tickets)) if all_tickets else 0,
                    message.from_user.first_name
                ),
                reply_markup=admin_buttons.get_admin_buttons(admins.ADMINS[message.from_user.id])
            )
        except KeyError:
            bot.send_message(
                message.from_user.id,
                "Выполните команду /start и попробуйте снова /admin"
            )
