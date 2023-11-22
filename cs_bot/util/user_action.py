from functools import wraps
from telebot import types


def on_user_action(db_ind=None, data_ind=None, data_type=None, add_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if all(arg is not None for arg in [db_ind, data_ind, data_type]):
                db = args[db_ind]
                data = args[data_ind]
                user = data.from_user
                chat_id = user.id
                username = user.username
                first_name = user.first_name
                last_name = user.last_name
                callback_data = None
                message = None
                if data_type is types.CallbackQuery:
                    callback_data = data.data
                if data_type is types.Message:
                    message = data.text
                if add_user is True:
                    db.update_user(chat_id, username, first_name, last_name, use_cache=True)
                db.add_user_action(chat_id, callback_data, message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
