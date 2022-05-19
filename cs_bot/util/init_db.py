import pymysql
import os
from pymysql.constants import CLIENT
from os.path import join as pj
from cs_bot import config


def init_db(db_name):
    query = open(pj(config.FILES_DIR, 'sql', 'init_db.sql'), 'r').read()
    query = query.replace('{{ DB_NAME }}', db_name)
    _exec(query)


def _exec(query):
    # print(query)
    connection = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()
