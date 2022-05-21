import random
from cs_bot.util.get_class_attributes import get_class_attributes
from cs_bot.util.format_if import format_if
from cs_bot.util.html import html_href
from cs_bot.util.poll import Poll, PollSeria


class Course:
    ALGORITHMS = 'algorithms'
    ALGORITHMS_2 = 'algorithms_2'
    CALCULUS = 'calculus'
    CPP = 'cpp'
    DISCRETE_MATH = 'discrete_math'
    INTRODUCTION_TO_CS = 'introduction_to_cs'
    LINEAR_ALGEBRA = 'linear_algebra'
    PYTHON = 'python'

    @staticmethod
    def names(ordering=False, beautify=False):
        courses = get_class_attributes(Course)
        if ordering:
            courses.sort(key=lambda course: Course.order_ind(course))
        if beautify:
            courses = list([Course.beautify(course) for course in courses])
        return courses

    @staticmethod
    def beautify(course_title):
        beautifier = {
            Course.ALGORITHMS: 'Алгоритмы и структуры данных',
            Course.ALGORITHMS_2: 'Алгоритмы и структуры данных - 2',
            Course.CALCULUS: 'Математический анализ',
            Course.CPP: 'C++',
            Course.DISCRETE_MATH: 'Дискретная математика',
            Course.INTRODUCTION_TO_CS: 'Введение в компьютерные науки',
            Course.LINEAR_ALGEBRA: 'Линейная алгебра',
            Course.PYTHON: 'Python'
        }
        return beautifier.get(course_title, '')

    @staticmethod
    def order_ind(course_title):
        course_order = {
            Course.ALGORITHMS: 2,
            Course.ALGORITHMS_2: 7,
            Course.CALCULUS: 6,
            Course.CPP: 5,
            Course.DISCRETE_MATH: 3,
            Course.INTRODUCTION_TO_CS: 0,
            Course.LINEAR_ALGEBRA: 4,
            Course.PYTHON: 1
        }
        return course_order[course_title]


class TestUnitPurpose:
    STUDY = 'study'
    COMPETE = 'compete'


def build_course_list_with_meta(chat_id, db):
    def course_priority(available_courses, completed_courses):
        def priority(course):
            if course not in available_courses:
                return 2
            if course in completed_courses:
                return 1
            return 0
        return priority

    course_prerequisites = db.get_all_courses_prerequisites(use_cache=True)
    completed_courses = db.get_completed_courses(chat_id)
    available_courses = set()
    for course in Course.names():
        if course_prerequisites[course].issubset(completed_courses):
            available_courses.add(course)
    courses = sorted(Course.names(ordering=True), key=course_priority(available_courses, completed_courses))
    return courses, available_courses, completed_courses


def source2str(source):
    # pattern: {author}: {title} ({year}) [{platform}] [{language}]
    href = html_href(
        format_if('{}: ', source['author'], condition=lambda args: None not in args) + source['title'],
        href=source['url'])
    string = ''.join([
        href,
        format_if(' ({})', source['year'], condition=lambda args: None not in args),
        format_if(' [{}]', source['platform'], condition=lambda args: None not in args),
        format_if(' [{}]', source['language'], condition=lambda args: None not in args)
    ])
    return string


def course_menu_reaction(course):
    reacts = {
        Course.ALGORITHMS: ['Как насчёт алгоритма захвата Вселенной? 🧐'],
        Course.ALGORITHMS_2: ['Как насчёт алгоритма захвата Вселенной за O(1)? 🧐'],
        Course.CALCULUS: ['Осторожно! Твои знания могут устремиться к бесконечно...\nчему-то бексонечному в общем.'],
        Course.CPP: ['Уже пробовал складывать строки?'],
        Course.DISCRETE_MATH: ['P=NP?', 'А ты правда умеешь считать сложность умножения?',
                               'Объединили как-то в одной комнате технарей и гуманитариев и никого не осталось.'],
        Course.INTRODUCTION_TO_CS: ['Правда ли что этот курс для тех, кто не умеет включать компьютер?\n'
                                    'Нет, он для тех, кто не может его выключить 🙃'],
        Course.LINEAR_ALGEBRA: ['Если ты не можешь понять, что куб вывернут наизнанку, '
                                'то нам и разговаривать не о чем!'],
        Course.PYTHON: ['...Питона приручить несложно, особенно маленького.\n'
                        'Главное следить, чтобы он не рисовал пружину. 🐍']
    }
    return random.choice(reacts.get(course, ['Никогда не знаешь, что может в жизни пригодиться.']))


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
