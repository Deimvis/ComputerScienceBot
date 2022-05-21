import time
from cs_bot.config import DB_CACHE_SIZE, DB_CACHE_TTL, DB_MAX_ROW_COUNT_FOR_CACHE
from cs_bot.util.get_class_attributes import get_class_attributes
from cs_bot.util.lru_cache import TimeBoundedLRUCache
from cs_bot.util.singleton import Singleton


class DBCache(TimeBoundedLRUCache, metaclass=Singleton):
    def __init__(self, cache_size=DB_CACHE_SIZE, cache_ttl=DB_CACHE_TTL):
        super().__init__(cache_size, cache_ttl)
        self._max_row_count_for_cache = DB_MAX_ROW_COUNT_FOR_CACHE

    def would_store(self, result):
        return len(result) < self._max_row_count_for_cache


class MySQLDatabaseInterface:
    def __init__(self, pool):
        self.pool = pool
        self._cache = DBCache()

    def _use_cache_mode(self, **kwargs):
        return 'use_cache' in kwargs and kwargs['use_cache'] is True

    def _exec(self, query, *args):
        connection = self.pool.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, [arg for arg in args])
        connection.commit()
        connection.close()
        return cursor.fetchall()

    def exec(self, query, *args, **kwargs):
        # print(query, args)
        query_cache_key = query + '#'.join(str(arg) for arg in args)
        if self._use_cache_mode(**kwargs) and query_cache_key in self._cache:
            query_result = self._cache[query_cache_key]
            if query_result is not None:
                # print('\tgot from cache')
                return self._cache[query_cache_key]
        result = self._exec(query, *args)
        if self._cache.would_store(result):
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

    def has_event(self, where, **kwargs):
        condition = ' and '.join(map(lambda key: key + '=%s', where.keys()))
        query = f'SHOW EVENTS WHERE {condition}'
        return len(self.exec(query, *where.values(), **kwargs)) > 0


class BaseMySQLDatabase(MySQLDatabaseInterface):
    class Table:
        USER = 'user'
        USER_ACTION = 'user_action'

        @staticmethod
        def names():
            return get_class_attributes(BaseMySQLDatabase.Table)

    def __init__(self, pool):
        super().__init__(pool)
        self._validate_db()

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

    def _validate_db(self):
        tables = super().show_tables(use_cache=True)
        for table in BaseMySQLDatabase.Table.names():
            assert table in tables, f'Table {table} not found in database.'

        where = {'Name': 'cleanup_user_action', 'Status': 'ENABLED'}
        assert super().has_event(where, use_cache=True), 'No enabled event `cleanup_user_action`.'
