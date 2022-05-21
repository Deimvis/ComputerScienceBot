import io
from telebot import types
from cs_bot.util.user_action import on_user_action
from cs_bot.roadmap import menu
from cs_bot.roadmap.util import build_roadmap


def _get_roadmap(db, chat_id):
    course_prerequisites = db.get_all_courses_prerequisites(use_cache=True)
    completed_courses = db.get_completed_courses(chat_id)
    available_courses = set()
    for course in db.get_course_list(use_cache=True):
        if course_prerequisites[course].issubset(completed_courses):
            available_courses.add(course)
    return build_roadmap(available_courses, completed_courses)


@on_user_action(db_ind=1, data_ind=2, data_type=types.Message, add_user=True)
def send_roadmap_menu(bot, db, message):
    roadmap = _get_roadmap(db, message.chat.id)
    bot.send_photo(message.chat.id, roadmap, reply_markup=menu.roadmap_menu)


@on_user_action(db_ind=1, data_ind=2, data_type=types.CallbackQuery)
def send_orig_roadmap_menu(bot, db, call):
    roadmap = _get_roadmap(db, call.message.chat.id)
    roadmap_bytes = io.BytesIO()
    roadmap.save(roadmap_bytes, format='png')
    bot.send_document(call.message.chat.id, roadmap_bytes.getvalue(), visible_file_name='Roadmap.png')
