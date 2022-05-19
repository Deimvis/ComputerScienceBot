from telebot import types


def build_start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_roadmap = types.KeyboardButton('/roadmap')
    button_courses = types.KeyboardButton('/courses')
    button_profile = types.KeyboardButton('/profile')
    button_help = types.KeyboardButton('/help')
    markup.add(button_roadmap)
    markup.add(button_courses)
    markup.add(button_profile)
    markup.add(button_help)
    return markup


start_menu = build_start_menu()
