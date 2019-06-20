# -*- coding: utf-8 -*-
import os
import re
import logging
import pathlib

from loguru import logger


def get_work_dir(workdir_name):
    workdir = os.path.join(
        os.getenv('XDG_DATA_HOME', os.path.expanduser("~/pyshella-toolkit")), workdir_name
    )

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    return workdir


def get_log_file(file_name):
    if os.environ.get('USER') == 'root':
        return os.path.join('/pyshella-toolkit/shared/logs', file_name)

    return os.path.join(
        get_work_dir('logs'), file_name
    )


def setup_logger(file, add_default_path=True, rotation="150 MB"):
    if add_default_path:
        file = get_log_file(file_name=file)

    format_ = "{time:DD-MM-YYYY-MM-DD at HH:mm:ss} | {level} | {extra[util]} | {message}"
    logger.add(file, format=format_, rotation=rotation)


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
