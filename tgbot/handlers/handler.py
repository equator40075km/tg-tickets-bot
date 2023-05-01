import os

from dotenv import load_dotenv
from telebot import TeleBot

from .help import help_handler
from .start import start_handler, start_callbacks

load_dotenv()

bot = TeleBot(token=os.getenv('TG_TOKEN'))

# handlers
start_handler.handle(bot)
help_handler.handle(bot)

# callbacks
start_callbacks.callback(bot)
