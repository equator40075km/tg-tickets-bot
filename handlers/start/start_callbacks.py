import json.decoder

from telebot import TeleBot
from telebot import types
from json import loads
from datetime import date

from helpers import dates
from . import start_buttons


MONTHS_CALLBACK_NAME = 'cb_m'
DAYS_CALLBACK_NAME = 'cb_d'


def callback(bot: TeleBot):
    def is_month_callback(sdata: str) -> bool:
        try:
            data: dict = loads(sdata)
        except json.decoder.JSONDecodeError:
            return False

        return data.get('cb') == MONTHS_CALLBACK_NAME

    @bot.callback_query_handler(func=lambda call: is_month_callback(call.data))
    def month_callback(call: types.CallbackQuery):
        data: dict = loads(call.data)
        _date: date = date.fromisoformat(data.get('date'))

        text = f'Месяц: {dates.get_month_name(_date.month)}.\n' \
               f'Какие даты вас интересуют?'

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=start_buttons.get_days_buttons(_date)
        )

    def is_days_callback(sdata: str) -> bool:
        try:
            data: dict = loads(sdata)
        except json.decoder.JSONDecodeError:
            return False

        return data.get('cb') == DAYS_CALLBACK_NAME

    @bot.callback_query_handler(func=lambda call: is_days_callback(call.data))
    def days_callback(call: types.CallbackQuery):
        data: dict = loads(call.data)
        _date: date = date.fromisoformat(data.get('date'))
        days: str = data.get('days')

        text = f'🫡 Я начал искать билеты на {dates.get_month_name(_date.month)}, на {days} числа\n\n' \
               f'⏳ Одну секунду... ⏳'

        bot.send_message(
            call.message.chat.id,
            text
        )
