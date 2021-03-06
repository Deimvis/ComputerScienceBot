from telebot import types
from cs_bot.util.callback import CallBuilder


def build_help_menu():
    markup = types.InlineKeyboardMarkup()
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('start'))
    markup.add(button_return)
    return markup


help_menu = build_help_menu()
