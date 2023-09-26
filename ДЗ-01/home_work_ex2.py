"""
This module provides functions to work with text data from files and strings.
"""

import io


def gen(f_obj, lst):
    if isinstance(f_obj, str):
        f_obj = from_str_to_file_obj(f_obj)

    if not isinstance(f_obj, io.TextIOWrapper):
        raise TypeError('UNEXPECTED TYPE')

    for line in f_obj:
        for el in lst:
            tmp = line.lower().split()
            if el.lower() in tmp:
                yield line.rstrip()


def from_str_to_file_obj(st):
    with open(file=st, mode='r', encoding='UTF-8', errors='replace') as f:
        return f
