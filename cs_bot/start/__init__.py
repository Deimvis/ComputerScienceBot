import cs_bot.start.handlers as handlers
import cs_bot.start.menu as menu
from cs_bot.util.apply import apply
from cs_bot.util.callback import CallChecker
from cs_bot.util.sql import BaseMySQLDatabase


def register_handlers(bot, connection):
    db = BaseMySQLDatabase(connection)
    bot.message_handler(commands=['start'])\
        (apply(bot, db)(handlers.start))
    bot.callback_query_handler(lambda call: CallChecker(call).like('start'))\
        (apply(bot, db)(handlers.start))
