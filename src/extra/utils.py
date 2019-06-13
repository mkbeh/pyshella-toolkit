# -*- coding: utf-8 -*-
import os
import re
import logging
import pathlib

from loguru import logger


def get_default_path():
    cwd = os.getcwd()
    return cwd.replace(
        'src', 'logs/'
    )


def setup_logger(file, add_default_path=True, enqueue=True, rotation="150 MB"):
    if add_default_path:
        file = os.path.join(get_default_path(), file)

    logger.add(file,
               format="{time:DD-MM-YYYY-MM-DD at HH:mm:ss} | {level} | {extra[util]} | {message}",
               enqueue=enqueue,
               rotation=rotation)


def setup_default_logger(logger_name, log_file, level=logging.INFO):
    default_logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    default_logger.setLevel(level)
    default_logger.addHandler(file_handler)

    return default_logger


def make_work_dir(dir_name):
    path = pathlib.Path(
        os.path.join(
            os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share")), dir_name
        )
    )
    path.mkdir(parents=True, exist_ok=True)

    return path


def get_file_path(dir_name, file_name):
    work_dir = make_work_dir(dir_name)

    return os.path.join(
        work_dir, file_name
    )


def range_to_nums(range_):
    return [i for i in range(*range_)]


def is_template_in_str(s, template=r'\w+'):
    pattern = re.compile(template)
    return True if re.search(pattern, s) else False


def count_lines(filename):
    with open(filename) as file:
        return sum(is_template_in_str(line) for line in file)


def clear_string(s):
    return s.strip(' \n')


def del_spec_chars_from_strings(*args):
    pattern = re.compile(r'[#!"\'/?]')
    result = []

    for arg in args:
        result.append(pattern.sub('', arg))

    return result
