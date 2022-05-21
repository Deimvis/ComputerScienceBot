from telebot import types
from cs_bot.util.callback import CallBuilder


def build_roadmap_menu():
    markup = types.InlineKeyboardMarkup()
    button_orig_roadmap = types.InlineKeyboardButton('Скачать Roadmap', callback_data=CallBuilder().make('roadmap', 'orig'))
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('start'))
    markup.add(button_orig_roadmap)
    markup.add(button_return)
    return markup


roadmap_menu = build_roadmap_menu()
