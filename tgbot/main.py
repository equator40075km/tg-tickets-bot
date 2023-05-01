from os import getenv
from handlers.handler import bot


if __name__ == "__main__":
    if getenv('TG_TOKEN') is None:
        print("TG_TOKEN not found in .env")
        exit(0)
    bot.infinity_polling()
