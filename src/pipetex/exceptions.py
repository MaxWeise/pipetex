""" Exception classes wich are used by the operations.

@author: Max Weise
created: 25.07.2022
"""

from pipetex.enums import SeverityLevels

from typing import Optional


class InternalException(Exception):
    """Is raised when an operation needs to communicate an error.

    This exception type is used when a runing operation can't execute properly
    due to an internal error. This can be e.g. a missing file, an unsucessfull
    call to a sys command or similar.  Every instance of this error type must
    contain a message and severity level. The message is used for logging and
    the severity level will be used to determine if the pipeline needs to stop
    or if it can still function.  Each operation os responisble for giving an
    appropriate message and severitylevel.


    Args:
        messgage: Exception message. Used to comunicate error to the user
            and to log statement.
        severity_level: Defines 'how bad' the error is and the further
            error handling strategy.
        error_tpye (optional): The type of error that is the cause of this
            exception.
    """

    # Public attributes
    message: str
    error_tpye: Optional[Exception]

    # Private attributes
    _severity_level: SeverityLevels

    def __init__(self, message: str, severity_level: SeverityLevels,
                 error_tpye: Optional[Exception] = None):
        """Instantiates an InternalException object.

        Args:
            messgage: Exception message. Used to comunicate error to the user
                and to log statement.
            severity_level: Defines 'how bad' the error is and the further
                error handling strategy.
            error_tpye (optional): The type of error that is the cause of this
                exception.
        """

        self.message = message
        self._severity_level = severity_level
        self.error_tpye = error_tpye

    @property
    def severity_level(self) -> int:
        """The severity level represented by an integer value."""
        return self._severity_level.value

    def __str__(self) -> str:
        """String representation of the exception type."""
        _errorType = ("InternalException" if not self.error_tpye
                      else self.error_tpye)
        return f"{_errorType} ({self.severity_level}) | {self.message}"

    def __repr__(self) -> str:
        """Repr method of the class. For now just use the super method."""
        return super().__repr__()

    # === Define order and comparison operations ===
    def __eq__(self, other) -> bool:
        """Overloads the == operator"""
        return bool(self.severity_level == other.severity_level)

    def __ge__(self, other) -> bool:
        """Overloads the >= operator"""
        return bool(self.severity_level >= other.severity_level)

    def __le__(self, other) -> bool:
        """Overloads the <= operator."""
        return bool(self.severity_level <= other.severity_level)

    def __lt__(self, other) -> bool:
        """Overloads the < operator."""
        return bool(self.severity_level < other.severity_level)

