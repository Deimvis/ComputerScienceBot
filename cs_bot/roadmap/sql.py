from collections import defaultdict
from cs_bot.util.sql import BaseMySQLDatabase
from cs_bot.util.get_class_attributes import get_class_attributes


class RoadmapMySQLDatabase(BaseMySQLDatabase):
    class Table:
        COURSE = 'course'
        COURSE_PREREQUISITE = 'course_prerequisite'
        USER_COMPLETED_COURSE = 'user_completed_course'

        @staticmethod
        def names():
            return get_class_attributes(RoadmapMySQLDatabase.Table)

    def __init__(self, pool):
        super().__init__(pool)
        self._validate_db()

    def get_course_list(self, **kwargs):
        courses = super().select_all(RoadmapMySQLDatabase.Table.COURSE, **kwargs)
        return list(map(lambda record: record['title'], courses))

    def get_all_courses_prerequisites(self, **kwargs):
        course_prerequisites = defaultdict(set)
        for record in super().select_all(RoadmapMySQLDatabase.Table.COURSE_PREREQUISITE, **kwargs):
            course_prerequisites[record['title']].add(record['prerequisite'])
        return course_prerequisites

    def get_completed_courses(self, chat_id, **kwargs):
        where = {'chat_id': chat_id}
        completed_courses = super().select(RoadmapMySQLDatabase.Table.USER_COMPLETED_COURSE, where, **kwargs)
        return set(map(lambda record: record['course_title'], completed_courses))

    def _validate_db(self):
        tables = super().show_tables(use_cache=True)
        for table in RoadmapMySQLDatabase.Table.names():
            assert table in tables, f'Table {table} not found in database.'
