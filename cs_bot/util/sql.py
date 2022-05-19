import time
from cs_bot.config import DB_CACHE_SIZE, DB_CACHE_TTL, DB_MAX_ROW_COUNT_FOR_CACHE
from cs_bot.util.lru_cache import TimeBoundedLRUCache


class MySQLDatabaseForceMode:
    def __init__(self, db):
        self._db = db

    def __enter__(self):
        self._db._force = True
        return self._db

    def __exit__(self):
        self._db._force = False


class MySQLDatabaseInterface:
    def __init__(self, pool, cache_size=DB_CACHE_SIZE, cache_ttl=DB_CACHE_TTL):
        self.pool = pool
        self._cache = TimeBoundedLRUCache(max_size=cache_size, ttl=cache_ttl)
        self._max_row_count_for_cache = DB_MAX_ROW_COUNT_FOR_CACHE

    def _use_cache_mode(self, **kwargs):
        return 'use_cache' in kwargs and kwargs['use_cache'] is True

    def _exec(self, query, *args):
        connection = self.pool.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, [arg for arg in args])
        connection.commit()
        connection.close()
        return cursor.rowcount, cursor.fetchall()

    def exec(self, query, *args, **kwargs):
        # print(query, args)
        query_cache_key = query + '#'.join(str(arg) for arg in args)
        if self._use_cache_mode(**kwargs) and query_cache_key in self._cache:
            query_result = self._cache[query_cache_key]
            if query_result is not None:
                # print('\tgot from cache')
                return self._cache[query_cache_key]
        row_count, result = self._exec(query, *args)
        if row_count < self._max_row_count_for_cache:
            self._cache[query_cache_key] = result
        return result

    def show_tables(self, **kwargs):
        query = 'SHOW TABLES'
        return set([next(iter(table_info.values())) for table_info in self.exec(query, **kwargs)])

    def count(self, table, where, **kwargs):
        condition = ' and '.join(map(lambda key: f'`{key}`=%s', where.keys()))
        query = f'SELECT COUNT(*) FROM `{table}` WHERE {condition}'
        return self.exec(query, *where.values(), **kwargs)[0]['COUNT(*)']

    def count_all(self, table, **kwargs):
        query = f'SELECT COUNT(*) FROM `{table}`'
        return self.exec(query, **kwargs)[0]['COUNT(*)']

    def count_distinct(self, table, distinct, where, **kwargs):
        condition = ' and '.join(map(lambda key: f'`{key}`=%s', where.keys()))
        query = f'SELECT COUNT(DISTINCT `{distinct}`) AS `res` FROM `{table}` WHERE {condition}'
        return self.exec(query, *where.values(), **kwargs)[0]['res']

    def exists(self, table, where, **kwargs):
        condition = ' and '.join(map(lambda key: f'`{key}`=%s', where.keys()))
        query = f'SELECT EXISTS(SELECT 1 FROM `{table}` WHERE {condition})'
        return all(self.exec(query, *where.values(), **kwargs)[0].values())

    def select(self, table, where, **kwargs):
        condition = ' and '.join(map(lambda key: f'`{key}`=%s', where.keys()))
        query = f'SELECT * FROM `{table}` WHERE {condition}'
        return self.exec(query, *where.values(), **kwargs)

    def select_all(self, table, **kwargs):
        query = f'SELECT * FROM `{table}`'
        return self.exec(query, **kwargs)

    def insert(self, table, record, **kwargs):
        schema = '(' + ', '.join(map(lambda key: f'`{key}`', record.keys())) + ')'
        values_schema = '(' + ','.join('%s' for key in record) + ')'
        query = f'INSERT INTO `{table}` {schema} VALUES {values_schema}'
        return self.exec(query, *record.values(), **kwargs)

    def replace(self, table, record, **kwargs):
        schema = '(' + ', '.join(map(lambda key: f'`{key}`', record.keys())) + ')'
        values_schema = '(' + ','.join('%s' for key in record) + ')'
        query = f'REPLACE INTO `{table}` {schema} VALUES {values_schema}'
        return self.exec(query, *record.values(), **kwargs)

    def delete(self, table, where, **kwargs):
        condition = ' and '.join(map(lambda key: key + '=%s', where.keys()))
        query = f'DELETE FROM {table} WHERE {condition}'
        return self.exec(query, *where.values(), **kwargs)


class BaseMySQLDatabase(MySQLDatabaseInterface):
    class Table:
        USER = 'user'
        USER_ACTION = 'user_action'

    def __init__(self, pool):
        super().__init__(pool)

    def has_user(self, chat_id, **kwargs):
        where = {'chat_id': chat_id}
        return super().exists(BaseMySQLDatabase.Table.USER, where, **kwargs)

    def get_user(self, chat_id, **kwargs):
        where = {'chat_id': chat_id}
        return super().select(BaseMySQLDatabase.Table.USER, where, **kwargs)[0]

    def update_user(self, chat_id, username, first_name, last_name, **kwargs):
        record = {'chat_id': chat_id, 'username': username, 'first_name': first_name,
                  'last_name': last_name, 'ts': int(time.time())}
        return super().replace(BaseMySQLDatabase.Table.USER, record, **kwargs)

    def remove_user(self, chat_id, **kwargs):
        where = {'chat_id': chat_id}
        return super().delete(BaseMySQLDatabase.Table.USER, where, **kwargs)

    def add_user_action(self, chat_id, callback_data, message, **kwargs):
        record = {'chat_id': chat_id, 'callback_data': callback_data, 'message': message, 'ts': int(time.time())}
        return super().insert(BaseMySQLDatabase.Table.USER_ACTION, record, **kwargs)


# init_db
# CREATE DATABASE IF NOT EXISTS computer_science_bot;
# CREATE TABLE IF NOT EXISTS user (
# chat_id BIGINT PRIMARY KEY,
# username TEXT,
# first_name TEXT,
# last_name TEXT,
# ts BIGINT,
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS course (
#     title VARCHAR(128) PRIMARY KEY,
#     description VARCHAR(512)
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS source (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     course_title VARCHAR(128) NOT NULL,
#     url VARCHAR(4096) NOT NULL,
#     title VARCHAR(128),
#     description TEXT,
#     `rank` INT,
#     language VARCHAR(32),
#     FOREIGN KEY (course_title)
#         REFERENCES course (title)
#         ON UPDATE RESTRICT
#         ON DELETE RESTRICT
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS test_unit (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     course_title VARCHAR(128),
#     purpose VARCHAR(512) NOT NULL,
#     difficulty VARCHAR(512),
#     question TEXT NOT NULL,
#     options TEXT NOT NULL COMMENT 'Json list',
#     answer_ind INT NOT NULL,
#     explanation VARCHAR(512),
#     FOREIGN KEY (course_title)
#         REFERENCES course (title)
#         ON UPDATE RESTRICT
#         ON DELETE RESTRICT
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS user_completed_test_unit (
#     chat_id BIGINT,
#     test_unit_id INT,
#     course_title VARCHAR(128),
#     purpose VARCHAR(512) NOT NULL,
#     difficulty VARCHAR(512),
#     is_answer_correct BOOLEAN NOT NULL,
#     ts BIGINT NOT NULL,
#     FOREIGN KEY (test_unit_id)
#         REFERENCES test_unit (id)
#         ON UPDATE RESTRICT
#         ON DELETE RESTRICT,
#     FOREIGN KEY (course_title)
#         REFERENCES course (title)
#         ON UPDATE RESTRICT
#         ON DELETE RESTRICT
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS user_completed_course (
#     chat_id BIGINT,
#     course_title VARCHAR(128),
#     ts BIGINT NOT NULL,
#     FOREIGN KEY (course_title)
#         REFERENCES course (title)
#         ON UPDATE RESTRICT
#         ON DELETE RESTRICT
# ) DEFAULT CHARSET=UTF8MB4;
# CREATE TABLE IF NOT EXISTS user_action (
#     chat_id BIGINT,
#     callback_data VARCHAR(512),
#     message VARCHAR(512),
#     ts BIGINT NOT NULL
# ) DEFAULT CHARSET=UTF8MB4;

