import os
import pymysql
import pytest
import cs_bot.config as config
from cs_bot.util.init_db import init_db


def _drop_test_db():
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute(f'DROP DATABASE IF EXISTS `{os.getenv("TEST_DB_NAME")}`')
    connection.commit()
    connection.close()


@pytest.fixture(scope='function')
def drop_test_db():
    _drop_test_db()


@pytest.fixture(scope='function')
def init_test_db():
    init_db(os.getenv('TEST_DB_NAME'))


@pytest.fixture(scope='session', autouse=True)
def prepare():
    _drop_test_db()
    yield
    _drop_test_db()
