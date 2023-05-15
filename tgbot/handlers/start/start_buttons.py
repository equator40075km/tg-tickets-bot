from telebot import types
from datetime import date
from json import dumps
from typing import List

from helpers import dates
from helpers.variables import MESSAGES, ADMIN_BUTTONS
from helpers.tg import TGAdmin
from . import start_callbacks


def get_months_buttons() -> types.InlineKeyboardMarkup:
    today: date = date.today()

    btn1 = types.InlineKeyboardButton(dates.get_month_name(today.month),
                                      callback_data=dumps({
                                          'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                          'date': today.isoformat()
                                      }))

    date2 = dates.get_future_month(1)
    btn2 = types.InlineKeyboardButton(dates.get_month_name(date2.month),
                                      callback_data=dumps({
                                          'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                          'date': date2.isoformat()
                                      }))

    date3 = dates.get_future_month(2)
    btn3 = types.InlineKeyboardButton(dates.get_month_name(date3.month),
                                      callback_data=dumps({
                                          'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                          'date': date3.isoformat()
                                      }))

    buttons = types.InlineKeyboardMarkup()
    buttons.add(btn1, btn2, btn3)
    return buttons


def get_days_buttons(_date: date) -> types.InlineKeyboardMarkup:
    buttons: List[types.InlineKeyboardButton] = []
    days1, days2, days3 = '', '', ''

    if _date.day == 10:
        days1 = '10'
    elif _date.day < 10:
        days1 = f'{_date.day} - 10'

    if days1:
        buttons.append(types.InlineKeyboardButton(
            days1,
            callback_data=dumps({
                'cb': start_callbacks.DAYS_CALLBACK_NAME,
                'date': _date.isoformat(),
                'days': days1
            })))

    if _date.day == 20:
        days2 = '20'
    elif _date.day < 20:
        if _date.day < 11:
            days2 = '11 - 20'
        else:
            days2 = f'{_date.day} - 20'

    if days2:
        buttons.append(types.InlineKeyboardButton(
            days2,
            callback_data=dumps({
              'cb': start_callbacks.DAYS_CALLBACK_NAME,
              'date': _date.isoformat(),
              'days': days2
            })))

    last_day: int = dates.get_month_last_day(_date)
    if _date.day == last_day:
        days3 = f'{last_day}'
    elif _date.day < last_day:
        if _date.day < 21:
            days3 = f'21 - {last_day}'
        else:
            days3 = f'{_date.day} - {last_day}'

    if days3:
        buttons.append(types.InlineKeyboardButton(
            days3,
            callback_data=dumps({
              'cb': start_callbacks.DAYS_CALLBACK_NAME,
              'date': _date.isoformat(),
              'days': days3
            })))

    markup = types.InlineKeyboardMarkup()
    markup.add(*buttons)
    return markup


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
