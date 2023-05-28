from telebot import types

from helpers.admins import TGAdmin
from helpers.variables import MESSAGES


def get_admin_buttons(admin: TGAdmin) -> types.ReplyKeyboardMarkup:
    admin_markup = types.ReplyKeyboardMarkup()

    admin_markup.add(MESSAGES['admin']['btns']['add_one_ticket'],
                     MESSAGES['admin']['btns']['remove_one_ticket'])

    admin_markup.add(MESSAGES['admin']['btns']['remove_overdue_tickets'],
                     MESSAGES['admin']['btns']['remove_inactive_users'])

    if admin.can_appoint:
        admin_markup.add(MESSAGES['admin']['btns']['appoint_admin'],
                         MESSAGES['admin']['btns']['remove_admin'])

    return admin_markup
