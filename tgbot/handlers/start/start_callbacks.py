import json.decoder
from datetime import date
from json import loads
from telebot import TeleBot, types
from typing import Union

from helpers.variables import MESSAGES
from helpers.api import TicketAPI, TGUserAPI
from helpers import dates
from . import start_buttons


MONTHS_CALLBACK_NAME = 'cb_M'
DAYS_CALLBACK_NAME = 'cb_D'
TICKETS_CALLBACK_NAME = 'cb_T'
RESTART_CALLBACK_NAME = 'cb_R'


def callback(bot: TeleBot):
    def callback_name(sdata: str) -> Union[str, None]:
        try:
            data: dict = loads(sdata)
        except json.decoder.JSONDecodeError:
            return None

        return data.get('cb')

    @bot.callback_query_handler(func=lambda call: callback_name(call.data) == MONTHS_CALLBACK_NAME)
    def month_callback(call: types.CallbackQuery):
        data: dict = loads(call.data)
        _date: date = date.fromisoformat(data.get('date'))

        bot.edit_message_text(
            text=MESSAGES['callback']['months'].format(dates.get_month_name(_date.month)),
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=start_buttons.get_multi_days_buttons(_date)
        )

    @bot.callback_query_handler(func=lambda call: callback_name(call.data) == DAYS_CALLBACK_NAME)
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

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=start_buttons.get_days_buttons(date_since, date_until)
        )

    @bot.callback_query_handler(func=lambda call: callback_name(call.data) == TICKETS_CALLBACK_NAME)
    def back_callback(call: types.CallbackQuery):
        data: dict = loads(call.data)
        since: date = date.fromisoformat(data.get('date'))
        until: Union[date, None] = None

        if 'until' in data:
            until: date = date.fromisoformat(data.get('until'))

        tg_user = TGUserAPI.get_tg_user(call.from_user.id)

        tickets = TicketAPI.get_tickets(tg_user['city'], since, until)
        if tickets is None or len(tickets) == 0:
            period: str = since.strftime(dates.DATE_FORMAT)
            if until:
                period += f" - {until.strftime(dates.DATE_FORMAT)}"
            bot.answer_callback_query(
                call.id,
                text=MESSAGES['user']['tickets_not_found'].format(period, tg_user['city'])
            )
            return

        for ticket in tickets:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=ticket['photo'],
                caption=f"{ticket['title']}\n\n"
                        f"Дата: {dates.get_human_date(ticket['date'])}\n"
                        f"Город отправления: {ticket['city']}\n\n"
                        f"→ {ticket['link']}\n\n"
                        f"{ticket['text']}"
            )

        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: callback_name(call.data) == RESTART_CALLBACK_NAME)
    def restart_callback(call: types.CallbackQuery):
        from handlers.handler import bot
        from .start_handler import start
        bot.delete_message(call.from_user.id, call.message.id)
        start(bot, call.from_user)
        bot.answer_callback_query(call.id)
