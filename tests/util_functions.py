""" This module contains helper functions for the test modules

The functions defined in this module can be usefull in different modules
of the test directory and are therefore outsurced in this file.

@author Max Weise
created 23.07.2022
"""

import os


def write_empty_file(file_name: str, file_extentions: str | list[str]):
    """Creates files for testing.

    Args:
        file_name: Name of file(s) to be created.
        file_extentions: .extention of file(s) to be created
    """
    if type(file_extentions) == list:
        for ex in file_extentions:
            with open(f"{file_name}.{ex}", "w+", encoding="utf-8"):
                pass

    else:
        ex = file_extentions
        with open(f"{file_name}.{ex}", "w+", encoding="utf-8"):
            pass


def remove_files(file_name: str):
    """ Removes files containing specified name.

    Args:
        file_name: Name of the file. Function searches this substring and
            removes the file.
    """

    list_of_files: list[str] = os.listdir(".")

    for f in list_of_files:
        if file_name in f:
            os.remove(f)

