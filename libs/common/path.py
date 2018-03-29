# coding=utf-8
# __author__ = 'zengyuetian'

import inspect
import os
import sys


def get_root_path():
    """
    get root dir
    :return:
    """
    parent_path = get_current_path()
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def get_root_parent_path():
    """
    get parent dir for root dir
    :return:
    """
    root_parent_path = os.path.dirname(get_root_path())
    return root_parent_path


def get_root_dir_name():
    return os.path.basename(get_root_path())


def get_current_path():
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    return parent_path


TOOLS_PATH = get_root_path() + "/tools"


if __name__ == "__main__":
    print get_root_path()
    print get_root_dir_name()



