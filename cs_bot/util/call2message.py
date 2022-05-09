from functools import wraps
from telebot import types


def call2message(func):
    @wraps(func)
    def wrapper(bot, db, obj, *args, **kwargs):
        message = None
        if isinstance(obj, types.CallbackQuery):
            message = obj.message
        elif isinstance(obj, types.Message):
            message = obj
        else:
            raise RuntimeError('object inside function is neither a message nor a call')
        return func(bot, db, message, *args, **kwargs)
    return wrapper
