# -*- coding: utf-8 -*-
import os
import re
import logging


def setup_logger(logger_name, log_file, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger


def make_work_dir(dir_name):
    path = os.path.join(
        os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share")), dir_name
    )

    if not os.path.exists(path):
        os.mkdir(path)

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
