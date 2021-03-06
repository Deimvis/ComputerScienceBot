import random
from telebot import types
from cs_bot.util.callback import CallParser
from cs_bot.util.html import html_bold
from cs_bot.util.user_action import on_user_action
from cs_bot.courses import menu
from cs_bot.courses.util import (
    Course,
    build_course_list_with_meta,
    source2str,
    course_menu_reaction,
    make_course_study_poll_seria,
    get_course_from_poll_seria
)


_DEFAULT_POLL_TIMEOUT = 30


@on_user_action(db_ind=1, data_ind=2, data_type=types.Message, add_user=True)
def send_course_list_menu(bot, db, message):
    text = '"Ученик, который учится без желания, — это птица без крыльев."\n<i>Саади</i>'
    courses, available_courses, completed_courses = build_course_list_with_meta(message.chat.id, db)
    bot.send_message(message.chat.id, text,
                     reply_markup=menu.build_course_list_menu(courses, available_courses, completed_courses))


@on_user_action(db_ind=1, data_ind=2, data_type=types.CallbackQuery)
def return_course_list_menu(bot, db, call):
    text = 'Новый курс - новые знания {}'.format(random.choices(['🧠', '🤯'], weights=[0.9, 0.1])[0])
    courses, available_courses, completed_courses = build_course_list_with_meta(call.message.chat.id, db)
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=menu.build_course_list_menu(courses, available_courses, completed_courses))


@on_user_action(db_ind=1, data_ind=2, data_type=types.CallbackQuery)
def send_course_menu(bot, db, call):
    course = CallParser(call).get(1)
    course_prerequisites = db.get_course_prerequisites(course, use_cache=True)
    completed_courses = db.get_completed_courses(call.message.chat.id)
    if not course_prerequisites.issubset(completed_courses):
        text = '\n'.join([
            'Для открытия данного курса необходимо пройти следующие курсы:',
            '<b>' + '</b>\n<b>'.join(
                map(lambda course: Course.beautify(course),
                    course_prerequisites - completed_courses)) + '</b>',
            'Посмотреть все зависимости курсов: /roadmap'
        ])
        return bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                     reply_markup=menu.unavailable_course_menu)
    text = course_menu_reaction(course)
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=menu.build_course_menu(course))


@on_user_action(db_ind=1, data_ind=2, data_type=types.CallbackQuery)
def send_sources_menu(bot, db, call):
    course = CallParser(call).get(1)
    sources = db.get_sources(course)
    if len(sources) == 0:
        text = 'Кажется, я ничего не смог найти.\nВозможно где-то сбои, попробуй повторить запрос позже.'
        return bot.send_message(call.message.chat.id, text)
    sources.sort(key=lambda source: source['rank'], reverse=True)
    text = '\n\n'.join(map(lambda source: source2str(source), sources))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          disable_web_page_preview=True, reply_markup=menu.build_source_menu(course))


@on_user_action(db_ind=1, data_ind=3, data_type=types.CallbackQuery)
def send_test_menu(bot, db, poll_controller, call):
    user = call.from_user
    db.update_user(user.id, user.username, user.first_name, user.last_name)
    course = CallParser(call).get(1)
    poll_seria = make_course_study_poll_seria(call.message.chat.id, db, course)
    poll = poll_seria.next_poll
    if poll is None:
        text = 'Тесты для курса не найдены.\nОтдохни немного, а мы постараемся всё исправить к твоему возвращению! 😉'
        return bot.send_message(call.message.chat.id, text)
    poll_call = bot.send_poll(call.message.chat.id, poll.question, poll.options, correct_option_id=poll.answer_ind,
                              explanation=poll.explanation, type='quiz',
                              is_anonymous=False, open_period=_DEFAULT_POLL_TIMEOUT)
    poll_id = poll_call.poll.id
    poll_seria.on_sending(poll_id)
    poll_controller.update(call.message.chat.id, None, poll_seria, new_poll_id=poll_id)


def send_next_test_unit(bot, db, poll_controller, call):
    poll_seria = poll_controller.get(call.user.id, call.poll_id)
    if poll_seria is None:
        text = 'Что-то случилось. Похоже на внутренню ошибку.\nНе переживай, скоро всё исправим! ☃️'
        return bot.send_message(call.user.id, text)
    poll_seria.on_answer(call.option_ids[0])
    poll = poll_seria.next_poll
    if poll is None:
        course = get_course_from_poll_seria(poll_seria)
        for poll in poll_seria:
            db.add_completed_test_unit(call.user.id, poll.test_unit_id, course, poll.purpose,
                                       poll.difficulty, poll.is_answer_correct)
        test_result = f'{poll_seria.correct_answers}/{poll_seria.size}'
        if poll_seria.size == poll_seria.correct_answers:
            db.add_completed_course(call.user.id, course)
            text = f'{html_bold(test_result)} 🔥🔥🔥\nТы молодец! Продолжай в том же духе! ✨'
            test_failed = False
        else:
            text = f'{html_bold(test_result)}\nНе унывай, попробуй снова! Всё получится! 🍀'
            test_failed = True
        return bot.send_message(call.user.id, text, reply_markup=menu.build_test_done_menu(course, test_failed))
    poll_call = bot.send_poll(call.user.id, poll.question, poll.options, correct_option_id=poll.answer_ind,
                              explanation=poll.explanation, type='quiz',
                              is_anonymous=False, open_period=_DEFAULT_POLL_TIMEOUT)
    poll_id = poll_call.poll.id
    poll_seria.on_sending(poll_id)
    poll_controller.update(call.user.id, call.poll_id, poll_seria, new_poll_id=poll_id)
