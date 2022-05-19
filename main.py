import pymysql
import pymysqlpool
import telebot
import cs_bot.common as common
import cs_bot.config as config
import cs_bot.courses as courses
import cs_bot.help as help
import cs_bot.profile as profile
import cs_bot.roadmap as roadmap
import cs_bot.start as start
from cs_bot.util.init_db import init_db


init_db(config.DB_NAME)
pool = pymysqlpool.ConnectionPool(
    size=config.MAX_USERS_ONLINE,
    maxsize=2 * config.MAX_USERS_ONLINE,
    pre_create_num=4,
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)
# connection = pymysql.connect(
#     host=config.DB_HOST,
#     port=config.DB_PORT,
#     user=config.DB_USER,
#     password=config.DB_PASSWORD,
#     database=config.DB_NAME,
#     cursorclass=pymysql.cursors.DictCursor
# )


bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode='HTML')
courses.register_handlers(bot, pool)
profile.register_handlers(bot, pool)
help.register_handlers(bot, pool)
roadmap.register_handlers(bot, pool)
start.register_handlers(bot, pool)
common.register_handlers(bot, pool)


if __name__ == '__main__':
    bot.polling()