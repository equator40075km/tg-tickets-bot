from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons = InlineKeyboardMarkup()
btn = InlineKeyboardButton("Написать нам", url="https://vk.com/im?media=&sel=-102627608")
buttons.add(btn)
