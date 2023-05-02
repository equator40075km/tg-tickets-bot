from telebot import TeleBot, types

from helpers.variables import MESSAGES, ADMIN_BUTTONS
from helpers import tg


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['text'])
    def text(message: types.Message):
        if message.chat.type != 'private':
            return

        if not tg.is_admin(message):
            bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES['text_not_admin']
            )
            return

        # TODO: проверить состояния админа и выполнить соответствующие действия
        # TODO: после действий обнулить состояние админа

        if message.text not in ADMIN_BUTTONS:
            bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES['admin_other_text']
            )
            return

        if message.text == MESSAGES['admin__add_one_ticket']:
            bot.send_message(
                chat_id=message.chat.id,
                text='Введите данные для добавления билета:\n. . .'
            )
            tg.ADMINS[message.from_user.id].adding_ticket = True
        elif message.text == MESSAGES['admin__remove_one_ticket']:
            bot.send_message(
                chat_id=message.chat.id,
                text='Выберите, какой билет хотите удалить:\n. . .'
            )
            tg.ADMINS[message.from_user.id].removing_ticket = True
        elif message.text == MESSAGES['admin__remove_overdue_tickets']:
            # TODO: удалить просроченные билеты
            bot.send_message(
                chat_id=message.chat.id,
                text='Просроченные билеты были успешно удалены.\nСервер говорит Вам спасибо🫡'
            )
        elif message.text == MESSAGES['admin__appoint_admin']:
            bot.send_message(
                chat_id=message.chat.id,
                text='Введите ID пользователя Telegram, которого вы хотите назначить администратором.\nНадеюсь, Вы не ошибетесь!'
            )
            tg.ADMINS[message.from_user.id].appointment = True
