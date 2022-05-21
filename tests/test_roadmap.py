import json
import os
import pytest
import random
import warnings
from os.path import join as pj
from pydantic import BaseModel, ValidationError, validator, root_validator
from typing import List, Optional
from cs_bot.config import FILES_DIR
from cs_bot.courses.util import Course
from cs_bot.roadmap.util import CombineMode, build_roadmap


ROADMAP_DIR = pj(FILES_DIR, 'roadmap')


def assert_file_exists(filepath):
    assert os.path.exists(filepath), ValidationError(f'File {filepath} doesn\'t exist.')


def assert_not_None_in(values):
    assert any(map(lambda value: value is not None, values)), ValidationError('All values are None.')


class ImageDefaultInfo(BaseModel):
    filename: Optional[str]
    combine_mode: Optional[str]
    width: Optional[int]
    height: Optional[int]

    @validator('filename')
    def file_exists(cls, v):
        if v is not None:
            assert_file_exists(pj(ROADMAP_DIR, v))
        return v

    @validator('combine_mode')
    def valid_combine_mode(cls, v):
        if v is not None:
            assert v in CombineMode.names(), f'Unknown combine mode: {v}'
        return v


class ImageInfo(ImageDefaultInfo):
    x_center: int
    y_center: int


class Background(BaseModel):
    filename: str
    width: Optional[int]
    height: Optional[int]

    @validator('filename')
    def file_exists(cls, v):
        assert_file_exists(pj(ROADMAP_DIR, v))
        return v


class Courses(BaseModel):
    class CourseDefaultItem(ImageDefaultInfo):
        check: ImageDefaultInfo

    class CourseItem(ImageInfo):
        course_title: str
        check: ImageInfo

        @validator('course_title')
        def course_title_is_valid(cls, v):
            assert v in Course.names(), f'Unknown course title: {v}'
            return v

    default: CourseDefaultItem
    items: List[CourseItem]

    @staticmethod
    def image_info_is_complete(item, default):
        assert_not_None_in([item.filename, default.filename])
        assert_not_None_in([item.combine_mode, default.combine_mode])
        assert_not_None_in([item.width, default.width])
        assert_not_None_in([item.height, default.height])

    @validator('items', each_item=True)
    def items_are_valid(cls, item, values, **kwargs):
        default = values['default']
        assert_file_exists(pj(ROADMAP_DIR, item.filename))
        cls.image_info_is_complete(item, default)
        cls.image_info_is_complete(item.check, default.check)
        return item


class RoadmapConfig(BaseModel):
    background: Background
    courses: Courses

    @staticmethod
    def image_size_is_valid(item, default, background):
        max_x = background.width
        max_y = background.height
        if max_x is None or max_y is None:
            warnings.warn('No background width/height. Can\'t validate item positions.')
            return
        width = item.width or default.width
        height = item.height or default.height
        x_center = item.x_center
        y_center = item.y_center
        assert 0 < x_center - width // 2, f'Image overflowing over the edge ({item["course_title"]})'
        assert 0 < y_center - height // 2, f'Image overflowing over the edge ({item["course_title"]})'
        assert x_center + width // 2 < max_x, f'Image overflowing over the edge ({item["course_title"]})'
        assert y_center + height // 2 < max_y, f'Image overflowing over the edge ({item["course_title"]})'

    @root_validator
    def items_are_valid(cls, values):
        background = values['background']
        courses = values['courses']
        default = courses.default
        for item in courses.items:
            cls.image_size_is_valid(item, default, background)
            cls.image_size_is_valid(item.check, default.check, background)
        return values


def test_roadmap_config():
    roadmap_dir = pj(FILES_DIR, 'roadmap')
    config = json.load(open(pj(roadmap_dir, 'config.json'), 'r'))
    RoadmapConfig.parse_obj(config)


@pytest.mark.parametrize('repeat', range(5))
def test_build_roadmap(repeat):
    available_courses = random.sample(Course.names(), random.randint(0, len(Course.names())))
    completed_courses = random.sample(available_courses, random.randint(0, len(available_courses)))
    build_roadmap(set(available_courses), set(completed_courses))
