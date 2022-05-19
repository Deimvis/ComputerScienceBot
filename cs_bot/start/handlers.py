from telebot import types
from cs_bot.start import menu
from cs_bot.util.user_action import on_user_action


@on_user_action(db_ind=1, data_ind=2, data_type=types.Message, add_user=True)
def send_start_menu(bot, db, message):
    bot.send_message(message.chat.id, 'Привет! 🖐\nЕсли заблудился, то команда /help укажет путь 💡', reply_markup=menu.start_menu)


@on_user_action(db_ind=1, data_ind=2, data_type=types.CallbackQuery)
def return_start_menu(bot, db, call):
    bot.send_message(call.message.chat.id, 'Куда отправимся в этот раз?', reply_markup=menu.start_menu)
