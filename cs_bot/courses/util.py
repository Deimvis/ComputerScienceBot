import random
from cs_bot.util.get_class_attributes import get_class_attributes
from cs_bot.util.html import html_hyperlink
from cs_bot.util.poll import Poll, PollSeria


class Course:
    ALGORITHMS = 'algorithms'

    @staticmethod
    def names():
        return get_class_attributes(Course)


class TestUnitPurpose:
    STUDY = 'study'
    COMPETE = 'compete'


def source2str(source):
    string = html_hyperlink(source['title'], source['url'])
    if source['language'] is not None:
        string += f' [{source["language"]}]'
    return string


def is_course_study_poll_seria(poll_controller, call):
    return poll_controller.has(call.user.id, call.poll_id, tags_like=[TestUnitPurpose.STUDY, Course.names()])


def make_course_study_poll_seria(chat_id, db, course, tests_count=5):
    all_test_units = db.get_tests(course, TestUnitPurpose.STUDY)
    test_units = random.sample(all_test_units, min(tests_count, len(all_test_units)))
    polls = [Poll(chat_id, test_unit) for test_unit in test_units]
    return PollSeria(polls, [TestUnitPurpose.STUDY, course])


def get_course_from_poll_seria(poll_seria):
    for tag in poll_seria.tags:
        if tag in Course.names():
            return tag

