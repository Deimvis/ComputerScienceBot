import cs_bot.start.handlers as handlers
from cs_bot.util.apply import apply
from cs_bot.util.callback import CallChecker
from cs_bot.util.sql import BaseMySQLDatabase


def register_handlers(bot, pool):
    db = BaseMySQLDatabase(pool)
    bot.message_handler(commands=['start'])\
        (apply(bot, db)(handlers.send_start_menu))
    bot.callback_query_handler(lambda call: CallChecker(call).like('start'))\
        (apply(bot, db)(handlers.return_start_menu))
