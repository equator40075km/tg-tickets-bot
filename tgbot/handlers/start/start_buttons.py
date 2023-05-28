from telebot import types
from datetime import date
from json import dumps
from typing import List

from helpers import dates
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


def get_multi_days_buttons(_date: date) -> types.InlineKeyboardMarkup:
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


def get_days_buttons(since: date, until: date) -> types.InlineKeyboardMarkup:
    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

    def get_day_inline_btn(_date: date) -> types.InlineKeyboardButton:
        return types.InlineKeyboardButton(
            text=_date.strftime(dates.DATE_FORMAT),
            callback_data=dumps({
                'cb': start_callbacks.TICKETS_CALLBACK_NAME,
                'date': _date.isoformat()
            })
        )

    tmp: date = since
    while tmp.day <= until.day:
        row = []
        try:
            for i in range(2):
                row.append(get_day_inline_btn(tmp))
                tmp = tmp.replace(day=tmp.day + 1)
            markup.add(*row)
        except ValueError:
            if row:
                markup.add(*row)
            break

    markup.add(types.InlineKeyboardButton(
        text=f"{since.strftime(dates.DATE_FORMAT)} - {until.strftime(dates.DATE_FORMAT)}",
        callback_data=dumps({
            'cb': start_callbacks.TICKETS_CALLBACK_NAME,
            'date': since.isoformat(),
            'until': until.isoformat()
        })
    ))

    markup.add(types.InlineKeyboardButton(
        text='Начать поиск заново',
        callback_data=dumps({
            'cb': start_callbacks.RESTART_CALLBACK_NAME,
            'cmd': 'start'
        })
    ))

    return markup
