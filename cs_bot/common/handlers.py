from telebot import types
from cs_bot.util.user_action import on_user_action


def common_poll_answer_handler(bot, db, poll_controller, call):
    text = 'Не смог найти контекста к твоему ответу.\nВозможно что-то пошло не по плану. 🙁'
    bot.send_message(call.user.id, text)


@on_user_action(db_ind=1, data_ind=2, data_type=types.Message)
def common_text_handler(bot, db, message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю :(')
