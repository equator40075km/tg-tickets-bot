import os

from dotenv import load_dotenv
from telebot import TeleBot

from .start import start_handler, start_callbacks
from .help import help_handler
from .city import city_handler
from .text import text_handler
from .photo import photo_handler

load_dotenv()

bot = TeleBot(token=os.getenv('TG_TOKEN'))

# handlers
start_handler.handle(bot)
help_handler.handle(bot)
city_handler.handle(bot)
text_handler.handle(bot)
photo_handler.handle(bot)

# callbacks
start_callbacks.callback(bot)
