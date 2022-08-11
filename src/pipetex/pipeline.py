"""Definition of a  pipeline object.

The pipeline executes multiple operations to compile a tex file to a
pdf file. The object is responsible for errorhandling and direction of values
returned form the operations.

@author: Max Weise
created: 29.07.2022
"""

from pipetex.utils import enums
from pipetex.utils import exceptions
from pipetex.operations import operations

from collections.abc import Callable
from typing import Any, Optional, Tuple

import logging


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]
OperationStep = Callable[[str, dict[str, Any]], Monad]


class Pipeline:

    file_name: str
    config_dict: dict[str, Any]
    order_of_operations: list[OperationStep]

    def __init__(self,
        file_name: str,
        create_bib: bool = False,
        create_glo: bool = False,
        verbose: bool = False,
        quiet: bool = False
    ) -> None:

        # Create sequence of operations
        self.order_of_operations = [
            operations.copy_latex_file,
            operations.remove_draft_option,
            operations.compile_latex_file
        ]

        if create_bib:
            self.order_of_operations.append(operations.create_bibliograpyh)

        if create_glo:
            self.order_of_operations.append(operations.create_glossary)

        self.order_of_operations.append(operations.compile_latex_file)
        self.order_of_operations.append(operations.clean_working_dir)

        # For some reason, the linter doesnt let me assign the dict as
        # an instance variable of pipeline
        self.config_dict = {    # type: ignore
            enums.ConfigDictKeys.VERBOSE.value: verbose,
            enums.ConfigDictKeys.QUIET.value: quiet,
            enums.ConfigDictKeys.FILE_PREFIX.value: "[piped]"
        }

        self.file_name = file_name

    def _set_error(
        self,
        current_error: Optional[exceptions.InternalException],
        new_error: exceptions.InternalException
    ) -> exceptions.InternalException:
        """Compares two errors and returns the one with higher severity_level.

        If the errors are equal in severity, the current_error will be kept, as it
        may be the root cause for any further errors.

        Args:
            current_error: The error which is currently most important.
            new_error: The error which is compared.

        returns
            InternalException: The error with higher severity_level.
        """
        rv = new_error
        if current_error and new_error < current_error:
            rv = current_error

        return rv

    def execute(self, file_name) -> Monad:
        rv_success: bool = True
        rv_error: Optional[exceptions.InternalException] = None

        for operation in self.order_of_operations:
            success, error = operation(file_name, self.config_dict)

            if error:
                match error.severity_level:
                    case enums.SeverityLevels.LOW:
                        logging.warning(
                            "There has been a minor issue during the "
                            f"execution of {operation} which did not affect "
                            "the flow of the pipeline. For more information "
                            "please see the logfiles."
                        )
                        logging.warning(
                        f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        rv_error = self._set_error(rv_error, error)

                    case enums.SeverityLevels.HIGH:
                        logging.warning(
                            "There has been an issue during the "
                            f"execution of {operation} which did not affect "
                            "the flow of the pipeline but my produce an "
                            "incorrect PDF file. For more information "
                            "please see the logfiles."
                        )
                        logging.debug(
                        f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        rv_error = self._set_error(rv_error, error)
                        rv_success = False

                    case enums.SeverityLevels.CRITICAL:
                        logging.warning(
                            "There has been an issue during the "
                            f"execution of {operation} which caused the "
                            "pipeline to stop its execution. Please see the "
                            "logfiles to for more information."
                        )
                        logging.critical(
                        f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        # Preemtive exit
                        return False, error

                    case _:
                        logging.warning("No recognized severity level to handle")

        # For some reason this gives an unboundError
        return rv_success, rv_error

