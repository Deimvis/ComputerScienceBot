from cs_bot.util.sql import BaseMySQLDatabase
from cs_bot.util.get_class_attributes import get_class_attributes


class ProfileMySQLDatabase(BaseMySQLDatabase):
    class Table:
        COURSE = 'course'
        TEST_UNIT = 'test_unit'
        USER_COMPLETED_COURSE = 'user_completed_course'
        USER_COMPLETED_TEST_UNIT = 'user_completed_test_unit'

        @staticmethod
        def names():
            return get_class_attributes(ProfileMySQLDatabase.Table)

    def __init__(self, pool):
        super().__init__(pool)
        self._validate_db()

    def get_course_count(self, **kwargs):
        return super().count_all(ProfileMySQLDatabase.Table.COURSE, **kwargs)

    def get_test_unit_count(self, **kwargs):
        return super().count_all(ProfileMySQLDatabase.Table.TEST_UNIT, **kwargs)

    def get_user_completed_course_count(self, chat_id, **kwargs):
        distinct = 'course_title'
        where = {'chat_id': chat_id}
        return super().count_distinct(ProfileMySQLDatabase.Table.USER_COMPLETED_COURSE, distinct, where, **kwargs)

    def get_user_completed_test_unit_count(self, chat_id, **kwargs):
        where = {'chat_id': chat_id}
        return super().count(ProfileMySQLDatabase.Table.USER_COMPLETED_TEST_UNIT, where, **kwargs)

    def get_user_completed_test_unit_with_correct_answer_count(self, chat_id, **kwargs):
        where = {'chat_id': chat_id, 'is_answer_correct': True}
        return super().count(ProfileMySQLDatabase.Table.USER_COMPLETED_TEST_UNIT, where, **kwargs)

    def get_user_completed_test_unit_distinct_count(self, chat_id, **kwargs):
        distinct = 'test_unit_id'
        where = {'chat_id': chat_id}
        return super().count_distinct(ProfileMySQLDatabase.Table.USER_COMPLETED_TEST_UNIT, distinct, where, **kwargs)

    def _validate_db(self):
        tables = super().show_tables(use_cache=True)
        for table in ProfileMySQLDatabase.Table.names():
            assert table in tables, f'Table {table} not found in database.'
