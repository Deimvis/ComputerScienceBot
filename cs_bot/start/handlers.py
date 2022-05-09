from telebot import types
from cs_bot.start.menu import start_menu
from cs_bot.util.call2message import call2message
from cs_bot.util.user_action import on_user_action


@call2message
@on_user_action(db_ind=1, data_ind=2, data_type=types.Message, add_user=True)
def start(bot, db, message):
    bot.send_message(message.chat.id, 'Привет! 🖐', reply_markup=start_menu)
