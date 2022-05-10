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
from cs_bot.util.init_db import init_test_db, drop_test_db


def simple_start():
    init_test_db()
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=os.getenv('TEST_DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

    bot = telebot.TeleBot(os.getenv('TEST_BOT_TOKEN'), parse_mode='HTML')
    courses.register_handlers(bot, connection)
    profile.register_handlers(bot, connection)
    start.register_handlers(bot, connection)
    common.register_handlers(bot, connection)
    bot.polling()


def test_env():
    assert isinstance(config.BOT_TOKEN, str)
    assert isinstance(config.DB_HOST, str)
    assert isinstance(config.DB_PORT, int)
    assert isinstance(config.DB_USER, str)
    assert isinstance(config.DB_PASSWORD, str)
    assert isinstance(config.DB_NAME, str)
    assert isinstance(config.DB_CACHE_SIZE, int)
    assert isinstance(config.DB_CACHE_TTL, int)
    assert isinstance(config.DB_MAX_ROW_COUNT_FOR_CACHE, int)
    assert isinstance(config.FILES_DIR, str)
    assert isinstance(config.MAX_USERS_ONLINE, int)


def test_testenv():
    assert isinstance(os.getenv('TEST_BOT_TOKEN'), str)
    assert isinstance(os.getenv('TEST_DB_NAME'), str)


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


@pytest.fixture(scope='session', autouse=True)
def on_finish():
    yield
    drop_test_db()
