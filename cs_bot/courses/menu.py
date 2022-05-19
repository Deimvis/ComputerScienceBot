from telebot import types
from cs_bot.util.callback import CallBuilder
from cs_bot.courses.util import Course


def build_course_list_menu(courses):
    markup = types.InlineKeyboardMarkup()
    for course in courses:
        button_with_course = types.InlineKeyboardButton(Course.beautify(course),
                                                       callback_data=CallBuilder().make('courses', course))
        markup.add(button_with_course)
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('start'))
    markup.add(button_return)
    return markup


def build_course_menu(course: str):
    markup = types.InlineKeyboardMarkup()
    button_sources = types.InlineKeyboardButton('Источники для изучения',
                                                callback_data=CallBuilder().make('sources', course))
    button_test = types.InlineKeyboardButton('Тест', callback_data=CallBuilder().make('test', course))
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('courses'))
    markup.add(button_sources)
    markup.add(button_test)
    markup.add(button_return)
    return markup


def build_unavailable_course_menu():
    markup = types.InlineKeyboardMarkup()
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('courses'))
    markup.add(button_return)
    return markup


def build_source_menu(course: str):
    markup = types.InlineKeyboardMarkup()
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('courses', course))
    markup.add(button_return)
    return markup


def build_test_done_menu(course: str, test_failed: bool):
    markup = types.InlineKeyboardMarkup()
    if test_failed is True:
        markup.add(types.InlineKeyboardButton('Попробовать снова', callback_data=CallBuilder().make('test', course)))
    button_return = types.InlineKeyboardButton('← Вернуться назад', callback_data=CallBuilder().make('courses', course))
    markup.add(button_return)
    return markup


unavailable_course_menu = build_unavailable_course_menu()
