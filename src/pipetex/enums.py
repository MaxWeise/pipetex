""" Enums shared in the project belong in this file.


@author: Max Weise
created: 25.07.2022
"""

import enum


class SeverityLevels(enum.IntEnum):
    """The levels of severity wich are used for exception handling.

    Higher levels indicate a more serious error. If neede values which are not
    a multiple of 10 can be inserted. However, the values must be integers.
    """

    LOW = 10
    HIGH = 20
    CRITICAL = 30


class ConfigDictKeys(enum.Enum):
    """This enum holds all allowed keys for the shared config dictionary.

    General Rules:
        Add keys as needed, but only if absolutely needed.
        string values have to be snake_case
    """

    NEW_NAME = "new_name"
    FILE_PREFIX = "file_prefix"
    VERBOSE = "verbose"
    QUIET = "quiet"

