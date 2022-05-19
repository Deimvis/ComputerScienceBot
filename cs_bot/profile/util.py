

def user_data2str(db, chat_id):
    user = db.get_user(chat_id)
    completed_courses = db.get_user_completed_course_count(chat_id)
    all_courses = db.get_course_count(use_cache=True)
    found_test_units = db.get_user_completed_test_unit_distinct_count(chat_id)
    all_test_units = db.get_test_unit_count(use_cache=True)
    correct_completed_test_units = db.get_user_completed_test_unit_with_correct_answer_count(chat_id)
    completed_test_units = db.get_user_completed_test_unit_count(chat_id)
    if completed_test_units > 0:
        correct_answer_rate = int(round(correct_completed_test_units * 100 / completed_test_units))
    else:
        correct_answer_rate = 0
    return '\n'.join([
        f'{user["first_name"]} {user["last_name"]} (@{user["username"]})',
        '---',
        f'Курсов изучено: {completed_courses}/{all_courses}',
        f'Учебных вопросов обнаружено: {found_test_units}/{all_test_units}',
        f'Доля правильных ответов: {correct_answer_rate}%'
    ])
