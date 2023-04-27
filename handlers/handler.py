import os
from telebot import TeleBot
from dotenv import load_dotenv

from handlers.start import start_handler, start_callbacks
from handlers.help import help_handler


load_dotenv()

bot = TeleBot(token=os.getenv('TG_TOKEN'))

start_handler.handle(bot)
help_handler.handle(bot)

start_callbacks.callback(bot)
