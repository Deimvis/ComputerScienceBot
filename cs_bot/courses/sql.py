import time
from cs_bot.util.sql import BaseMySQLDatabase
from cs_bot.util.get_class_attributes import get_class_attributes
from cs_bot.courses.util import Course


class CoursesMySQLDatabase(BaseMySQLDatabase):
    class Table:
        COURSE = 'course'
        SOURCE = 'source'
        TEST_UNIT = 'test_unit'
        USER_COMPLETED_COURSE = 'user_completed_course'
        USER_COMPLETED_TEST_UNIT = 'user_completed_test_unit'

        @staticmethod
        def names():
            return get_class_attributes(CoursesMySQLDatabase.Table)

    def __init__(self, connection):
        super().__init__(connection)
        self.connection = connection
        self._validate_db()

    def get_sources(self, course, **kwargs):
        where = {'course_title': course}
        return super().select(CoursesMySQLDatabase.Table.SOURCE, where, **kwargs)

    def get_tests(self, course, purpose, **kwargs):
        where = {'course_title': course, 'purpose': purpose}
        return super().select(CoursesMySQLDatabase.Table.TEST_UNIT, where, **kwargs)

    def add_completed_test_unit(self, chat_id, test_unit_id, course, purpose, difficulty, is_answer_correct, **kwargs):
        record = {'chat_id': chat_id, 'test_unit_id': test_unit_id, 'course_title': course, 'purpose': purpose,
                  'difficulty': difficulty, 'is_answer_correct': is_answer_correct, 'ts': int(time.time())}
        return super().insert(CoursesMySQLDatabase.Table.USER_COMPLETED_TEST_UNIT, record, **kwargs)

    def add_completed_course(self, chat_id, course, **kwargs):
        record = {'chat_id': chat_id, 'course_title': course, 'ts': int(time.time())}
        return super().replace(CoursesMySQLDatabase.Table.USER_COMPLETED_COURSE, record, **kwargs)

    def _validate_db(self):
        tables = super().show_tables()
        for table in CoursesMySQLDatabase.Table.names():
            assert table in tables, f'Table {table} not found in database.'
        for course in Course.names():
            assert super().exists(CoursesMySQLDatabase.Table.COURSE, {'title': course}),\
                    f'Course `{course}` not found in `{CoursesMySQLDatabase.Table.COURSE}`'
        # TODO:
        # Check events
