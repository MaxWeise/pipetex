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

from tests.shared_fixtures import testfile_tex, config_dict, testfile_tex_no_draft_option   # noqa: E501

import os
import pytest
from typing import Optional, Tuple


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]

def test_remove_draft_option(testfile_tex, config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = testfile_tex

    underTest: Monad = operations.remove_draft_option(file_name, config_dict)

    with open(f"{file_name}.tex", "r") as f:
        lines_in_testfile: list[str] = [line.rstrip() for line in f]

    assert underTest[0]
    assert not underTest[1]
    assert "draft" not in lines_in_testfile[0]
    assert len(lines_in_testfile) == 4


def test_remove_draft_option_fileNotFound(config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    underTest = operations.remove_draft_option(
        "not_a_file",
        config_dict
    )

    assert not underTest[0]
    assert type(underTest[1].severity_level) == int
    assert 20 < underTest[1].severity_level <= 30


def test_remove_draft_option_draftOptionNotFound(testfile_tex_no_draft_option,
                                                 config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = testfile_tex_no_draft_option

    with open(f"{file_name}.tex", "r") as f:
        lines_befor_runing_test: list[str] = [line.rstrip() for line in f]

    underTest = operations.remove_draft_option(
        testfile_tex_no_draft_option,
        config_dict
    )

    with open(f"{file_name}.tex", "r") as f:
        lines_after_runing_test: list[str] = [line.rstrip() for line in f]

    assert lines_after_runing_test == lines_befor_runing_test
    assert not underTest[0]
    assert type(underTest[1].severity_level) == int
    assert underTest[1].severity_level <= 10


def test_copy_file(testfile_tex, config_dict):
    """Tests that the working file is copied correctly."""
    file_name = testfile_tex
    new_file_name = f"[piped]_{file_name}"

    underTest = operations.copy_latex_file(file_name, config_dict)
    expectedNewName: str = config_dict[enums.ConfigDictKeys.NEW_NAME.value]

    assert underTest[0]
    assert not underTest[1]
    assert f"{new_file_name}.tex" in os.listdir()
    assert f"{new_file_name}" == expectedNewName
    assert f"{file_name}.tex" in os.listdir()


def test_copy_file_fileNotFound(testfile_tex, config_dict):
    """Tests that the working file is copied correctly."""

    # file_name = testfile_tex
    underTest = operations.copy_latex_file("Not a testfile", config_dict)

    assert not underTest[0]
    assert type(underTest[1].severity_level) == int
    assert 20 < underTest[1].severity_level <= 30


