import time
from collections import defaultdict
from cs_bot.util.sql import BaseMySQLDatabase
from cs_bot.util.get_class_attributes import get_class_attributes
from cs_bot.courses.util import Course


class CoursesMySQLDatabase(BaseMySQLDatabase):
    class Table:
        COURSE = 'course'
        COURSE_PREREQUISITE = 'course_prerequisite'
        SOURCE = 'source'
        TEST_UNIT = 'test_unit'
        USER_COMPLETED_COURSE = 'user_completed_course'
        USER_COMPLETED_TEST_UNIT = 'user_completed_test_unit'

        @staticmethod
        def names():
            return get_class_attributes(CoursesMySQLDatabase.Table)

    def __init__(self, pool):
        super().__init__(pool)
        self._validate_db()

    def get_sources(self, course, **kwargs):
        where = {'course_title': course}
        return super().select(CoursesMySQLDatabase.Table.SOURCE, where, **kwargs)

    def get_tests(self, course, purpose, **kwargs):
        where = {'course_title': course, 'purpose': purpose}
        return super().select(CoursesMySQLDatabase.Table.TEST_UNIT, where, **kwargs)

    def get_all_courses_prerequisites(self, **kwargs) -> defaultdict[set]:
        course_prerequisites = defaultdict(set)
        for record in super().select_all(CoursesMySQLDatabase.Table.COURSE_PREREQUISITE, **kwargs):
            course_prerequisites[record['title']].add(record['prerequisite'])
        return course_prerequisites

    def get_course_prerequisites(self, course, **kwargs) -> set:
        course_prerequisites = set()
        where = {'title': course}
        for record in super().select(CoursesMySQLDatabase.Table.COURSE_PREREQUISITE, where, **kwargs):
            course_prerequisites.add(record['prerequisite'])
        return course_prerequisites

    def get_completed_courses(self, chat_id, **kwargs) -> set:
        where = {'chat_id': chat_id}
        completed_courses = super().select(CoursesMySQLDatabase.Table.USER_COMPLETED_COURSE, where, **kwargs)
        return set(map(lambda record: record['course_title'], completed_courses))

    def add_completed_test_unit(self, chat_id, test_unit_id, course, purpose, difficulty, is_answer_correct, **kwargs):
        record = {'chat_id': chat_id, 'test_unit_id': test_unit_id, 'course_title': course, 'purpose': purpose,
                  'difficulty': difficulty, 'is_answer_correct': is_answer_correct, 'ts': int(time.time())}
        return super().insert(CoursesMySQLDatabase.Table.USER_COMPLETED_TEST_UNIT, record, **kwargs)

    def add_completed_course(self, chat_id, course, **kwargs):
        record = {'chat_id': chat_id, 'course_title': course, 'ts': int(time.time())}
        return super().replace(CoursesMySQLDatabase.Table.USER_COMPLETED_COURSE, record, **kwargs)

    def _validate_db(self):
        tables = super().show_tables(use_cache=True)
        for table in CoursesMySQLDatabase.Table.names():
            assert table in tables, f'Table {table} not found in database.'
        for course in Course.names():
            assert super().exists(CoursesMySQLDatabase.Table.COURSE, {'title': course}),\
                   f'Course `{course}` not found in `{CoursesMySQLDatabase.Table.COURSE}`'
