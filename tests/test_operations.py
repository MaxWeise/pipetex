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

from tests.shared_fixtures import testfile_tex
from tests.shared_fixtures import config_dict
from tests.shared_fixtures import testfile_tex_no_draft_option
from tests.shared_fixtures import dirty_working_dir_files


import os
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


def test_clean_working_dir(dirty_working_dir_files, config_dict):
    """Tests that the working dir gets cleaned properly."""

    test_file: str = dirty_working_dir_files

    underTest = operations.clean_working_dir(test_file, config_dict)
    current_dir = os.listdir()

    assert underTest[0]
    assert not underTest[1]

    for ex in ['tex', 'aux', 'pdf', 'glo', 'bib']:
        assert f"{test_file}.{ex}" not in current_dir
    assert "DEPLOY" in current_dir
    assert f"{test_file}.pdf" in os.listdir("./DEPLOY")


def test_clean_working_dir_FolderAlreadyExists(dirty_working_dir_files,
                                               config_dict):
    """Tests that the function executes properly."""

    underTest = operations.clean_working_dir(
        dirty_working_dir_files,
        config_dict
    )

    assert not underTest[0]
    assert type(underTest[1].severity_level) == int
    assert underTest[1].severity_level <= 10

    for ex in file_extentions:
        assert f"{test_file}.{ex}" not in current_dir
    assert "DEPLOY" in current_dir
    assert f"{test_file}.pdf" in os.listdir("./DEPLOY")
    ...


def test_clean_working_dir_PdfFileNotFound(dirty_working_dir_files,
                                           config_dict):
    """Tests that the correct error type is thrown."""
    test_file = dirty_working_dir_files

    os.remove(f"{test_file}.pdf")
    underTest = operations.clean_working_dir(
        dirty_working_dir_files,
        config_dict
    )

    assert not underTest[0]

    assert type(underTest[1].severity_level) == int
    assert 10 < underTest[1].severity_level <= 20

    for ex in ['tex', 'aux', 'pdf', 'glo', 'bib']:
        assert f"{test_file}.{ex}" not in current_dir

