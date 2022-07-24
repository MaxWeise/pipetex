""" Operations and utility functions used in the pipeline class

The functions described in this module define a single operation which will be
executed by the pipeline object. All public functions must adhere to the same
signature so the pipeline can dynamically execute them one by one.

@author: Max Weise
created: 23.07.2022
"""

import os
import subprocess
from typing import Any


# function signature: Callable[str, dict[str, Any]] -> Any

# === Preparation of file / working dir ===

def remove_draft_option(file_name: str, config_dict: dict[str, Any]) -> Any:
    """Removes the draft option from a tex file.

    Each tex file contains a class definition, where additional options can
    be specified, including the draft option (for more info, see the project
    specification or the latex documentation). This function finds this option
    and removes it, leaving a compilable tex file.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    """
    ...


# === Compilation / Creation of aux files / Generating LaTeX artifacts ===

def compile_latex_file(file_name: str, config_dict: dict[str, Any]) -> Any:
    """Compiles the file with to create a PDF file.

    Compiles a file by using a latex engine on the filename given to the
    function.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    """

    if f"{file_name}.tex" not in os.listdir():
        raise FileNotFoundError(
            f"The file {file_name}.tex is not found in the current "
            "working directory"
        )

    argument_list: list[str] = ["pdflatex", "-quiet", f"{file_name}.tex"]

    # TODO: Remove quiet option if specified in config_dict

    try:
        subprocess.call(argument_list)
    except Exception as e:
        # TODO: Logg exception
        print(e)


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

    """
    ...


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

    """
    ...


# === tear down / clean up processes ===

def clean_working_dir(file_name: str, config_dict: dict[str, Any]) -> Any:
    """Cleans the working directory from any generated files.

    Removes unwanted / redundant auxiliary files. Moves the created PDF
    document to a specified folder.

    Args:
        file_name: The name of the file to be compiled. Does not contain any
            file extension.
        config_dict: Dictionary containing further settings to run the engine.

    """
    ...

