from cs_bot.util.apply import apply
from cs_bot.profile import handlers
from cs_bot.profile.sql import ProfileMySQLDatabase


def register_handlers(bot, connection):
    db = ProfileMySQLDatabase(connection)
    bot.message_handler(commands=['profile'])\
        (apply(bot, db)(handlers.send_profile_menu))
