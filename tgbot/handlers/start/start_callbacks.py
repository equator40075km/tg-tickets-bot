import json.decoder
from datetime import date
from json import loads
from telebot import TeleBot
from telebot import types

from helpers.variables import MESSAGES
from helpers.api import TicketAPI, TGUserAPI
from helpers.dates import get_month_name, get_human_date
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

        bot.send_message(
            call.message.chat.id,
            MESSAGES['callback']['months'].format(get_month_name(_date.month)),
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
        date_: date = date.fromisoformat(data.get('date'))
        days: str = data.get('days')

        if days.find('-') != -1:
            since, until = days.replace(' ', '').split('-')
        else:
            since, until = days, days

        date_since = date_.replace(day=int(since))
        date_until = date_.replace(day=int(until))
        tg_user = TGUserAPI.get_tg_user(call.from_user.id)

        tickets = TicketAPI.get_tickets(tg_user['city'], date_since, date_until)
        if tickets is None or len(tickets) == 0:
            bot.send_message(
                call.message.chat.id,
                MESSAGES['user']['tickets_not_found'].format(days)
            )
            return

        for ticket in tickets:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=ticket['photo'],
                caption=f"{ticket['title']}\n\n"
                        f"Дата: {get_human_date(ticket['date'])}\n"
                        f"Город отправления: {ticket['city']}\n\n"
                        f"→ {ticket['link']}\n\n"
                        f"{ticket['text']}"
            )
