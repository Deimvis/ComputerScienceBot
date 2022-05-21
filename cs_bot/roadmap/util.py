import json
from os.path import join as pj
from PIL import Image
from cs_bot.config import FILES_DIR
from cs_bot.util.get_class_attributes import get_class_attributes


class CombineMode:
    PASTE = 'paste'
    ALPHA_COMPOSITE = 'alpha_composite'

    @staticmethod
    def names():
        return get_class_attributes(CombineMode)


def _combine(background, foreground, combine_mode, x=0, y=0):
    if combine_mode == CombineMode.PASTE:
        background.paste(foreground, (x, y), foreground)
    elif combine_mode == CombineMode.ALPHA_COMPOSITE:
        background = Image.alpha_composite(background, foreground)
    else:
        raise RuntimeError('Roadmap | Got unknown combine_mode')
    return background


def _add_image(background, item, default, roadmap_dir, grayscale=False):
    filename = item.get('filename') or default['filename']
    img = Image.open(pj(roadmap_dir, filename)).convert('RGBA')
    if grayscale is True:
        img = img.convert('LA').convert('RGBA')
    combine_mode = item.get('combine_mode', default['combine_mode'])
    width = item.get('width', default['width'])
    height = item.get('height', default['height'])
    x = item['x_center'] - width // 2
    y = item['y_center'] - height // 2
    return _combine(background, img, combine_mode, x, y)


def build_roadmap(available_courses, completed_courses):
    roadmap_dir = pj(FILES_DIR, 'roadmap')
    config = json.load(open(pj(roadmap_dir, 'config.json'), 'r'))
    background = Image.open(pj(roadmap_dir, config['background']['filename'])).convert('RGBA')
    default = config['courses']['default']

    for item in config['courses']['items']:
        grayscale = item['course_title'] not in available_courses
        background = _add_image(background, item, default, roadmap_dir, grayscale)
        if item['course_title'] in completed_courses:
            background = _add_image(background, item['check'], default['check'], roadmap_dir, grayscale)

    return background
