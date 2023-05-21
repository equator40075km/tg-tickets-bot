import time
from typing import List, Union
from helpers.jsons_loader import load_messages


# хранилище сообщений-ответов для пользователей и обрабатываемых сообщений от админов
MESSAGES: Union[dict, None] = load_messages()
if MESSAGES is None:
    print('MESSAGES is None!')
    exit(0)


# названия кнопок типа KeyboardButton для админов
ADMIN_BUTTONS: List[str] = [btn_name for _, btn_name in MESSAGES['admin']['btns'].items()]


ADMIN_ALERT_INTERVAL: int = 60 * 60 * 4
LAST_ADMIN_ALERT_TIME: time = time.time() - ADMIN_ALERT_INTERVAL
