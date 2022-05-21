from cs_bot.util.apply import apply
from cs_bot.util.callback import CallChecker
from cs_bot.roadmap import handlers
from cs_bot.roadmap.sql import RoadmapMySQLDatabase


def register_handlers(bot, pool):
    db = RoadmapMySQLDatabase(pool)
    bot.message_handler(commands=['roadmap'])\
        (apply(bot, db)(handlers.send_roadmap_menu))
    bot.callback_query_handler(func=lambda call: CallChecker(call).like('roadmap', 'orig'))\
        (apply(bot, db)(handlers.send_orig_roadmap_menu))
