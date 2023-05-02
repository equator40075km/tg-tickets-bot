from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons = InlineKeyboardMarkup()
buttons.add(InlineKeyboardButton("Написать нам", url="https://vk.com/im?media=&sel=-102627608"))


admin_buttons = InlineKeyboardMarkup()
admin_buttons.add(InlineKeyboardButton("Связаться с «Создателем»", url="https://t.me/n10vV"))
admin_buttons.add(InlineKeyboardButton("Связаться с Директором", url="https://t.me/business_jet"))
