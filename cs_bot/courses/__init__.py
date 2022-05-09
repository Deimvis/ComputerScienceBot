from cs_bot.util.apply import apply
from cs_bot.util.callback import CallChecker
from cs_bot.util.poll import PollSeriaController
from cs_bot.courses import handlers
from cs_bot.courses.util import Course, is_course_study_poll_seria
from cs_bot.courses.sql import CoursesMySQLDatabase


def register_handlers(bot, connection):
    db = CoursesMySQLDatabase(connection)
    poll_controller = PollSeriaController()
    bot.message_handler(commands=['courses'])\
        (apply(bot, db)(handlers.send_course_list_menu))
    bot.callback_query_handler(func=lambda call: CallChecker(call).like('courses'))\
        (apply(bot, db)(handlers.return_course_list_menu))
    bot.callback_query_handler(func=lambda call: CallChecker(call).like('courses', Course.names()))\
        (apply(bot, db)(handlers.send_course_menu))
    bot.callback_query_handler(func=lambda call: CallChecker(call).like('sources', Course.names()))\
        (apply(bot, db)(handlers.send_sources_menu))
    bot.callback_query_handler(func=lambda call: CallChecker(call).like('test', Course.names()))\
        (apply(bot, db, poll_controller)(handlers.send_test_menu))
    bot.poll_answer_handler(func=lambda call: is_course_study_poll_seria(poll_controller, call))\
        (apply(bot, db, poll_controller)(handlers.send_next_test_unit))


