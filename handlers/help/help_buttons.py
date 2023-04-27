from telebot import types


btn_cancel = types.KeyboardButton('Отмена 🚫')

confirm_send = types.ReplyKeyboardMarkup( resize_keyboard=True )
btn_confirm_send = types.KeyboardButton('Отправить ✅')
confirm_send.row(btn_confirm_send, btn_cancel)
