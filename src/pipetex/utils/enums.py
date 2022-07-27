""" Enums shared in the project belong in this file.


@author: Max Weise
created: 25.07.2022
"""

import enum


class SeverityLevels(enum.IntEnum):
    """The levels of severity wich are used for exception handling."""

    LOW = 10
    HIGH = 20
    CRITICAL = 30

