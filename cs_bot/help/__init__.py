import cs_bot.help.handlers as handlers
import cs_bot.help.menu as menu
from cs_bot.util.apply import apply
from cs_bot.util.sql import BaseMySQLDatabase


def register_handlers(bot, pool):
    db = BaseMySQLDatabase(pool)
    bot.message_handler(commands=['help'])\
        (apply(bot, db)(handlers.send_help_menu))
