import telebot
import multiprocessing
import os
import pymysql
import pytest
import cs_bot.common as common
import cs_bot.config as config
import cs_bot.courses as courses
import cs_bot.profile as profile
import cs_bot.start as start


def simple_start():
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode='HTML')
    courses.register_handlers(bot, connection)
    profile.register_handlers(bot, connection)
    start.register_handlers(bot, connection)
    common.register_handlers(bot, connection)
    bot.polling()


def test_simple_start():
    try:
        p = multiprocessing.Process(target=simple_start)
        p.start()
        p.join(10)
        assert p.is_alive()
        p.terminate()
        p.join()
    except Exception as e:
        pytest.fail('Bot did not start:\n{}'.format(e))
