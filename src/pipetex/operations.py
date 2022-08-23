""" Operations and utility functions used in the pipeline class

The functions described in this module define a single operation which will be
executed by the pipeline object. All public functions must adhere to the same
signature so the pipeline can dynamically execute them one by one.

@author: Max Weise
created: 23.07.2022
"""

from pipetex import exceptions
from pipetex.enums import SeverityLevels, ConfigDictKeys

import datetime
import os
import re
import shutil
import subprocess
from typing import Any, Optional, Tuple


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]


# === Preparation of file / working dir ===
def copy_latex_file(file_name: str, config_dict: dict[str, Any]) -> Monad:
    """Create a working copy of the specified latex file.

    To avoid losing data or corrupting the latex file a copy is created. The
    copy can be identified by a prefix added in this function. The new file
    name is written in the config dict. It is the responsibility of the
    dict owner to update the name of the working file accordingly.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to
            comunicate exceptions and how to handle them back to the calling
            interface.
            [Please see class definition]
        Raised Levels: CRITICAL
    """

    if f"{file_name}.tex" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.tex is not in the directory.",
            SeverityLevels.CRITICAL
        )

        return False, ex

    file_prefix: str = config_dict[ConfigDictKeys.FILE_PREFIX.value]
    new_name: str = f"{file_prefix}_{file_name}"
    shutil.copy(f'{file_name}.tex', f'{new_name}.tex')

    config_dict[ConfigDictKeys.NEW_NAME.value] = new_name

    return True, None


def remove_draft_option(file_name: str, config_dict: dict[str, Any]) -> Monad:
    """Removes the draft option from a tex file.

    Each tex file contains a class definition, where additional options can
    be specified, including the draft option (for more info, see the project
    specification or the latex documentation). This function finds this option
    and removes it, leaving a compilable tex file.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to comunicate
            exceptions and how to handle them back to the calling interface.
            [Please see class definition]
        Raised Levels: CRITICAL, LOW
    """

    if f"{file_name}.tex" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.tex is not found in the current "
            "working directory",
            SeverityLevels.CRITICAL
        )

        return False, ex

    with open(f"{file_name}.tex", "r", encoding="utf-8") as read_file:
        lines_of_file: list[str] = [line for line in read_file]

    class_line = lines_of_file[0]

    options_list = re.findall(r"\[(.+?)\]", class_line)[0].split(",")
    doc_class = re.findall(r"\{(.+?)\}", class_line)

    try:
        options_list.pop(options_list.index(" draft"))
    except ValueError:
        ex = exceptions.InternalException(
            "Draft option is not in the class definition",
            SeverityLevels.LOW
        )

        return False, ex

    options_string = "[" + ",".join(options_list) + "]"
    doc_class = "{" + doc_class[0] + "}"

    lines_of_file[0] = f"\\documentclass{options_string}{doc_class}\n"

    with open(f"{file_name}.tex", "w", encoding="utf-8") as write_file:
        write_file.writelines(lines_of_file)

    return True, None


# === Compilation / Creation of aux files / Generating LaTeX artifacts ===
def compile_latex_file(file_name: str, config_dict: dict[str, Any]) -> Monad:
    """Compiles the file with to create a PDF file.

    Compiles a file by using a latex engine on the filename given to the
    function.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to comunicate
            exceptions and how to handle them back to the calling interface.
            [Please see class definition]
        Raised Levels: CRITICAL
    """

    if f"{file_name}.tex" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.tex is not found in the current "
            "working directory",
            SeverityLevels.CRITICAL
        )

        return False, ex

    argument_list: list[str] = ["pdflatex", "-quiet", f"{file_name}.tex"]
    if config_dict[ConfigDictKeys.VERBOSE.value]:
        argument_list.pop(argument_list.index("-quiet"))

    subprocess.call(argument_list)

    return True, None


def _is_bibfile_present() -> bool:
    """Searches bibliography file recursively in the current working dir.

    Returns:
        bool: True, if the bibliography file is present somewhere in the
            working dir or its subdirs."""
    file_types: list[str] = []
    for _, _, files in os.walk(os.getcwd()):
        for f in files:
            if "." in f:
                parts = f.split(".")
                file_types.append(parts[-1])

    return "bib" in file_types


def create_bibliograpyh(file_name: str, config_dict: dict[str, Any]) -> Any:
    """Creates a bibliography file.

    Runs a script to create a bibliography based on the entries in the main tex
    file. This does not hinder the creation of the PDF file.  There must be a
    .bfc file present for the script to run properly. The .bfc file is created
    when a tex file containing bibliography entries is compiled.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to comunicate
            exceptions and how to handle them back to the calling interface.
            [Please see class definition]
        Raised Levels: HIGH
    """
    if f"{file_name}.bcf" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.bcf has not been created. "
            "Bibliography can not be created.",
            SeverityLevels.HIGH
        )

        return False, ex

    if not _is_bibfile_present():
        ex = exceptions.InternalException(
            "There is no bibliography file in the current project. "
            "Cant create bibliography.",
            SeverityLevels.HIGH
        )

        return False, ex

    argument_list: list[str] = ["biber", "-q", f"{file_name}"]

    if config_dict[ConfigDictKeys.VERBOSE.value]:
        argument_list.pop(argument_list.index("-q"))

    subprocess.call(argument_list)

    return True, None


def create_glossary(file_name: str, config_dict: dict[str, Any]) -> Any:
    """Creates a glossary file.

    Runs a script to create a glossary based on the entries in the main tex
    file. This does not hinder the creation of the PDF file.  There must be a
    .glo and .ist file present for the script to run properly. Thees files are
    created when a tex file containing glossary entries is compiled.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to comunicate
            exceptions and how to handle them back to the calling interface.
            [Please see class definition]
        Raised Levels: HIGH
    """
    if f"{file_name}.glo" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.glo has not been created. "
            "Glossary can not be created.",
            SeverityLevels.HIGH
        )

        return False, ex

    if f"{file_name}.ist" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.ist has not been created. "
            "Glossary can not be created.",
            SeverityLevels.HIGH
        )

        return False, ex

    if f"{file_name}.aux" not in os.listdir():
        ex = exceptions.InternalException(
            f"The file {file_name}.aux has not been created. "
            "Glossary can not be created.",
            SeverityLevels.HIGH
        )

        return False, ex

    argument_list: list[str] = ["makeglossaries", "-q", f"{file_name}"]

    if config_dict[ConfigDictKeys.VERBOSE.value]:
        argument_list.pop(argument_list.index("-q"))

    subprocess.call(argument_list)

    return True, None


# === tear down / clean up processes ===
def _move_pdf_file(file_name, new_file_name: Optional[str] = None) -> Monad:
    """Moves pdf file to seperate folder.

    To avoid that the created pdf file is deleted by the clean up process, this
    function creates a dedicated folder and moves the pdf file there.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    Raises:
        InternalException: Indicates an internal error and is used to comunicate
            exceptions and how to handle them back to the calling interface.
            [Please see class definition]
        Raised Levels: HIGH
    """
    _exeption = None
    _successvalue = True

    if not new_file_name:
        cur_date = datetime.datetime.now()
        formatted_date = cur_date.strftime("%Y_%m_%d_%H_%M")
        new_file_name = f"{formatted_date}_{file_name}"

    # Create Folder
    try:
        os.makedirs("DEPLOY")
    except FileExistsError:
        _exeption = exceptions.InternalException(
            "Folder already exists. Proceed as intended.",
            SeverityLevels.LOW
        )

        _successvalue = False

    try:
        shutil.move(f"{file_name}.pdf", "./DEPLOY")
        old_name = os.path.join(".", "DEPLOY", f"{file_name}.pdf")
        new_name = os.path.join(".", "DEPLOY", f"{new_file_name}.pdf")
        os.rename(old_name, new_name)
    except FileNotFoundError:
        _exeption = exceptions.InternalException(
            "The pdf document could not be found. Perhaps it was not created?",
            SeverityLevels.CRITICAL
        )

        _successvalue = False

    return _successvalue, _exeption


def clean_working_dir(file_name: str, config_dict: dict[str, Any],
                      new_file_name: Optional[str] = None) -> Monad:
    """Cleans the working directory from any generated files.

    Removes unwanted / redundant auxiliary files. Moves the created PDF
    document to a specified folder.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    Returns:
        Monad: Tuple which contains a boolean to indicate success of the
            function. If its true, the second value will be None. If its
            false, the second value will contain an InternalException object
            containing further information.

    """
    _success: bool = True
    _exception: Optional[exceptions.InternalException] = None

    _success, _exception = _move_pdf_file(file_name, new_file_name)

    if _exception and _exception.severity_level >= 20:
        return False, _exception

    for file in os.listdir():
        if config_dict[ConfigDictKeys.FILE_PREFIX.value] in file:
            os.remove(file)

    return _success, _exception

