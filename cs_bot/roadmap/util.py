import json
from os.path import join as pj
from PIL import Image, ImageOps
from cs_bot.config import FILES_DIR


def build_roadmap(available_courses, completed_courses):
    roadmap_dir = pj(FILES_DIR, 'roadmap')
    config = json.load(open(pj(roadmap_dir, 'config.json'), 'r'))
    background = Image.open(pj(roadmap_dir, config['background']['filename'])).convert('RGBA')
    course_default_width = config['courses']['default_width']
    course_default_height = config['courses']['default_height']

    completed = {'python'}

    for item in config['courses']['items']:
        img = Image.open(pj(roadmap_dir, item['filename'])).convert('RGBA')
        if item['course_title'] in completed:
            # TODO: mark that course is completed
            pass
        if item['course_title'] not in available_courses:
            img = img.convert('LA')
        width = item.get('width', course_default_width)
        height = item.get('height', course_default_height)
        x = item['x_center'] - width // 2
        y = item['y_center'] - height // 2
        background.paste(img, (x, y), img)

    return background
