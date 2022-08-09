""" Test file for the operations of the pipeline.

For now, all operations will be tested in this file. It is forseen though, that
the file will grow to a point where it is no longer practical and the
testcases need to be split into different files. How this will be done is not
entirely clear right now.

@author Max Weise
created 23.07.2022
"""

from src.pipetex.operations import operations
from src.pipetex.utils import enums, exceptions
from tests import util_functions


import os
import pytest
import shutil
from typing import Optional, Tuple


# === Fixtures ===
FILE_PREFIX = "[piped]"

@pytest.fixture
def simple_testfile():
    """Generates a simple tex file to run tests with."""
    file_name = "test_file"
    with open(f"{file_name}.tex", "w+", encoding="utf-8") as f:
        f.write(
            "\\documentclass[a4paper, draft, 12pt]{article}\n"
            "\\begin{document}\n"
            "This is a testfile\n"
            "\\end{document}\n"
        )

    yield file_name

    util_functions.remove_files(file_name)


@pytest.fixture
def simple_testfile_no_draft():
    """Generates a simple tex file to run tests with."""
    file_name = "test_file"
    with open(f"{file_name}.tex", "w+", encoding="utf-8") as f:
        f.write(
            "\\documentclass[a4paper, 12pt]{article}\n"
            "\\begin{document}\n"
            "This is a testfile\n"
            "\\end{document}\n"
        )

    yield file_name

    util_functions.remove_files(file_name)


@pytest.fixture
def dirty_working_dir():
    """Create some auxiliary files to 'pollute' the working dir."""
    file_name = f"{FILE_PREFIX}_test_file"
    ex = ['tex', 'aux', 'pdf', 'glo', 'bib']
    util_functions.write_empty_file(file_name, ex)

    yield file_name

    util_functions.remove_files(file_name)

    util_functions.remove_files("not_removed")

    if "DEPLOY" in os.listdir():
        shutil.rmtree("DEPLOY")


@pytest.fixture
def config_dict():
    return {"file_prefix": "[piped]"}


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]


def test_remove_draft_option(simple_testfile, config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = simple_testfile

    success, error = operations.remove_draft_option(file_name, config_dict)

    with open(f"{file_name}.tex", "r") as f:
        lines_in_testfile: list[str] = [line.rstrip() for line in f]

    assert success
    assert not error
    assert "draft" not in lines_in_testfile[0]
    assert len(lines_in_testfile) == 4


def test_remove_draft_option_fileNotFound(config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = "not_a_file"
    success, error = operations.remove_draft_option(file_name, config_dict)

    assert not success
    assert error
    assert type(error.severity_level) == int
    assert 20 < error.severity_level <= 30


def test_remove_draft_option_draftOptionNotFound(simple_testfile_no_draft,
                                                 config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = simple_testfile_no_draft

    with open(f"{file_name}.tex", "r") as f:
        lines_befor_runing_test: list[str] = [line.rstrip() for line in f]

    success, error = operations.remove_draft_option(
        simple_testfile_no_draft,
        config_dict
    )

    with open(f"{file_name}.tex", "r") as f:
        lines_after_runing_test: list[str] = [line.rstrip() for line in f]

    assert lines_after_runing_test[1:] == lines_befor_runing_test[1:]
    assert not success
    assert error
    assert type(error.severity_level) == int
    assert error.severity_level <= 10


def test_copy_file(simple_testfile, config_dict):
    """Tests that the working file is copied correctly."""
    file_name = simple_testfile
    new_file_name = f"{FILE_PREFIX}_{file_name}"

    success, error = operations.copy_latex_file(file_name, config_dict)
    expectedNewName: str = config_dict[enums.ConfigDictKeys.NEW_NAME.value]

    assert success
    assert not error
    assert f"{new_file_name}.tex" in os.listdir()
    assert f"{new_file_name}" == expectedNewName
    assert f"{file_name}.tex" in os.listdir()


def test_copy_file_fileNotFound(config_dict):
    """Tests that the working file is copied correctly."""

    success, error = operations.copy_latex_file("Not a testfile", config_dict)

    assert not success
    assert error
    assert type(error.severity_level) == int
    assert 20 < error.severity_level <= 30


def test_clean_working_dir(dirty_working_dir, config_dict):
    """Tests that the working dir gets cleaned properly."""

    # write a testfile which should not be removed by the method
    not_removed = "not_removed"
    with open(f"{not_removed}.tex", "w+") as f:
        pass

    test_file = dirty_working_dir

    success, error = operations.clean_working_dir(test_file, config_dict)
    current_dir = os.listdir()

    assert success
    assert not error

    for ex in ['tex', 'aux', 'pdf', 'glo', 'bib']:
        assert f"{test_file}.{ex}" not in current_dir
    assert f"{not_removed}.tex" in current_dir
    assert "DEPLOY" in current_dir
    assert f"{test_file}.pdf" in os.listdir("./DEPLOY")


def test_clean_working_dir_FolderAlreadyExists(dirty_working_dir, config_dict):
    """Tests that the function executes properly."""

    test_file = dirty_working_dir
    # Create the folder as part of the env setup
    os.mkdir("DEPLOY")
    success, error = operations.clean_working_dir(
        dirty_working_dir,
        config_dict
    )
    current_dir = os.listdir()

    assert not success
    assert error
    assert type(error.severity_level) == int
    assert error.severity_level <= 10

    for ex in ['tex', 'aux', 'pdf', 'glo', 'bib']:
        assert f"{test_file}.{ex}" not in current_dir
    assert "DEPLOY" in current_dir
    assert f"{test_file}.pdf" in os.listdir("./DEPLOY")


def test_clean_working_dir_PdfFileNotFound(dirty_working_dir, config_dict):
    """Tests that the correct error type is thrown."""
    test_file = dirty_working_dir

    os.remove(f"{test_file}.pdf")
    success, error = operations.clean_working_dir(
        dirty_working_dir,
        config_dict
    )

    assert not success
    assert error
    assert type(error.severity_level) == int
    assert 20 < error.severity_level <= 30

