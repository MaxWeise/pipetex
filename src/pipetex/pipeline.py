"""Definition of a  pipeline object.

The pipeline executes multiple operations to compile a tex file to a
pdf file. The object is responsible for errorhandling and direction of values
returned form the operations.

@author: Max Weise
created: 29.07.2022
"""

from pipetex import enums
from pipetex import exceptions
from pipetex import operations

from collections.abc import Callable
from typing import Any, Optional, Tuple

import logging


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]
OperationStep = Callable[[str, dict[str, Any]], Monad]


class Pipeline:
    """Representation of a pipeline object. Runs different tasks on the file.

    The pipeline keeps a reference of which operations should be run in which
    order. Also the pipeline will comunicate errors to the user by using
    logging stements.

    Common Usage:
        p = Pipeline(file_name, True, False, False, False)
        p.execute(p.file_name)

    Attributes:
        file_name: Name of the file which should be processed.
        config_dict: Contains metadata which should be shared
             with the operations.
        oder_of_operations: List of operations which will be run on the file.
    """

    file_name: str
    config_dict: dict[str, Any]
    order_of_operations: list[OperationStep]

    def __init__(self,
                 file_name: str,
                 create_bib: Optional[bool] = False,
                 create_glo: Optional[bool] = False,
                 verbose: Optional[bool] = False,
                 ) -> None:
        """Initialize a pipeline object.

        Args:
            file_name: Name of the file which will be processed.
            create_bib: Create a bibliography. Defaults to false.
            create_glo: Create a glossary. Defaults to false.
            verbose: Print console output of latex engines. Defaults to false.
        """
        # Creating object logger
        self.logger = logging.getLogger("main.pipeline")

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
            enums.ConfigDictKeys.FILE_PREFIX.value: "[piped]"
        }

        self.file_name = file_name

    def _set_error(
        self,
        current_error: Optional[exceptions.InternalException],
        new_error: exceptions.InternalException
    ) -> exceptions.InternalException:
        """Compares two errors and returns the one with higher severity_level.

        If the errors are equal in severity, the current_error will be kept, as
        it may be the root cause for any further errors.

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

    # TODO: Refactor this method to make it physically smaller.
    def execute(self, file_name) -> Monad:
        """Executes the operations defined by the constructor.

        Args:
            file_name: The file which is processed by the operations.

        Returns:
            Monad: Tuple which holds a value indicating the success of the
                pipeline and an error value if success is false.
        """
        rv_success: bool = True
        rv_error: Optional[exceptions.InternalException] = None
        local_file_name = file_name

        for operation in self.order_of_operations:
            self.logger.debug(f"Now executing: {operation}")
            success, error = operation(local_file_name, self.config_dict)

            try:
                local_file_name = self.config_dict[
                    enums.ConfigDictKeys.NEW_NAME.value
                ]
            except KeyError:
                # log this exception
                # for now, eat it
                pass

            if error:
                match error.severity_level:
                    case enums.SeverityLevels.LOW:
                        self.logger.warning(
                            "There has been a minor issue during the "
                            f"execution of {operation} which did not affect "
                            "the flow of the pipeline. For more information "
                            "please see the logfiles."
                        )

                        self.logger.warning(
                            f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        rv_error = self._set_error(rv_error, error)

                    case enums.SeverityLevels.HIGH:
                        self.logger.warning(
                            "There has been an issue during the "
                            f"execution of {operation} which did not affect "
                            "the flow of the pipeline but my produce an "
                            "incorrect PDF file. For more information "
                            "please see the logfiles."
                        )

                        self.logger.debug(
                            f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        rv_error = self._set_error(rv_error, error)
                        rv_success = False

                    case enums.SeverityLevels.CRITICAL:
                        self.logger.warning(
                            "There has been an issue during the "
                            f"execution of {operation} which caused the "
                            "pipeline to stop its execution. Please see the "
                            "logfiles to for more information."
                        )

                        self.logger.critical(
                            f""" Operation {operation}

                             SeverityLevel: {error.severity_level}
                             Error Message: {error.message}
                             Error Tpye: {error.error_tpye}"""
                        )

                        # Preemtive exit
                        return False, error

                    case _:
                        self.logger.warning(
                            "No recognized severity level to handle"
                        )
                        pass

        return rv_success, rv_error

