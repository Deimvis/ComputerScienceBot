from telebot import types
from cs_bot.util.user_action import on_user_action
from cs_bot.profile import menu
from cs_bot.profile.util import user_data2str


@on_user_action(db_ind=1, data_ind=2, data_type=types.Message, add_user=True)
def send_profile_menu(bot, db, message):
    text = user_data2str(db, message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=menu.profile_menu)
