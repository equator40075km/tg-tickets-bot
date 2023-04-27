from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from json import dumps

from helpers import dates
from . import start_callbacks


def get_months_buttons() -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    today: date = date.today()

    btn1 = InlineKeyboardButton(dates.get_month_name(today.month),
                                callback_data=dumps({
                                    'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                    'date': today.isoformat()
                                }))

    date2 = dates.get_future_month(1)
    btn2 = InlineKeyboardButton(dates.get_month_name(date2.month),
                                callback_data=dumps({
                                    'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                    'date': date2.isoformat()
                                }))

    date3 = dates.get_future_month(2)
    btn3 = InlineKeyboardButton(dates.get_month_name(date3.month),
                                callback_data=dumps({
                                    'cb': start_callbacks.MONTHS_CALLBACK_NAME,
                                    'date': date3.isoformat()
                                }))

    buttons.add(btn1, btn2, btn3)
    return buttons


def get_days_buttons(_date: date) -> InlineKeyboardMarkup:
    days1: str = '1 - 10'
    btn1 = InlineKeyboardButton(days1,
                                callback_data=dumps({
                                    'cb': start_callbacks.DAYS_CALLBACK_NAME,
                                    'date': _date.isoformat(),
                                    'days': days1
                                }))

    days2: str = '11 - 20'
    btn2 = InlineKeyboardButton(days2,
                                callback_data=dumps({
                                    'cb': start_callbacks.DAYS_CALLBACK_NAME,
                                    'date': _date.isoformat(),
                                    'days': days2
                                }))

    days3: str = f'21 - {dates.get_month_last_day(_date)}'
    btn3 = InlineKeyboardButton(days3,
                                callback_data=dumps({
                                    'cb': start_callbacks.DAYS_CALLBACK_NAME,
                                    'date': _date.isoformat(),
                                    'days': days3
                                }))

    buttons = InlineKeyboardMarkup()
    buttons.add(btn1, btn2, btn3)
    return buttons
