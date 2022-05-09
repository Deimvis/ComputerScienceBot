import cs_bot.common.handlers as handlers
from cs_bot.util.apply import apply
from cs_bot.util.callback import CallChecker
from cs_bot.util.sql import BaseMySQLDatabase
from cs_bot.util.poll import PollSeriaController


def register_handlers(bot, connection):
    db = BaseMySQLDatabase(connection)
    poll_controller = PollSeriaController()
    bot.poll_answer_handler(func=lambda call: True) \
        (apply(bot, db, poll_controller)(handlers.common_poll_answer_handler))
    bot.message_handler(content_types=['text'])\
        (apply(bot, db)(handlers.common_text_handler))
