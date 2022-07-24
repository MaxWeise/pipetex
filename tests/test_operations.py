""" Test file for the operations of the pipeline.

For now, all operations will be tested in this file. It is forseen though, that
the file will grow to a point where it is no longer practical and the
testcases need to be split into different files. How this will be done is not
entirely clear right now.

@author Max Weise
created 23.07.2022
"""

from src.pipetex.operations import operations
from tests.test_helpers.util_functions import remove_files

import os
import pytest
import shutil


@pytest.fixture
def testfile_tex():
    test_file_name = "test_file"
    shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
    yield test_file_name

    # remove texput.log specifically
    file_list = os.listdir()
    os.remove("texput.log") if "texput.log" in file_list else ...

    remove_files(test_file_name)


@pytest.fixture
def testfile_tex_no_draft_option():
    test_file_name = "test_file_no_draft"
    shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
    yield test_file_name

    remove_files(test_file_name)


@pytest.fixture
def testfile_bib():
    test_file_name = "test_file_bib"
    shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
    shutil.copy(f"./test_assets/{test_file_name}.bib", ".")
    shutil.copy(f"./test_assets/{test_file_name}.bcf", ".")
    yield test_file_name

    remove_files(test_file_name)


@pytest.fixture
def testfile_bib_no_bcf():
    test_file_name = "test_file_bib"
    shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
    shutil.copy(f"./test_assets/{test_file_name}.bib", ".")
    yield test_file_name

    remove_files(test_file_name)


@pytest.fixture
def config_dict():
    return {}


def test_compile_latex_file(testfile_tex, config_dict):
    """Tests the compilation of latex files. """
    # Setup Code
    file_name = testfile_tex

    # run test function
    underTest = operations.compile_latex_file(file_name, config_dict)   # noqa: F841, E501

    # assert statements
    assert f"{file_name}.pdf" in os.listdir("."), (
        f"The file {file_name}.pdf does not exist"
    )
    assert os.stat(f"{file_name}.pdf").st_size > 0


def test_compile_latex_file_fileNotFound(config_dict):
    """Tests that the compilation function raises an appropriate error. """
    # run test function
    with pytest.raises(FileNotFoundError):
        underTest = operations.compile_latex_file("not_a_file", config_dict)    # noqa: F841, E501


def test_remove_draft_option(testfile_tex, config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = testfile_tex

    # run test function
    underTest = operations.remove_draft_option(file_name, config_dict)  # noqa: F841, E501

    with open(f"{file_name}.tex", "r") as f:
        lines_in_testfile: list[str] = [line.rstrip() for line in f]

    # assert conditions
    assert "draft" not in lines_in_testfile[0]
    assert len(lines_in_testfile) == 4


def test_remove_draft_option_fileNotFound(config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    # run test function
    with pytest.raises(FileNotFoundError):
        underTest = operations.remove_draft_option("not_a_file", config_dict)   # noqa: F841, E501


def test_remove_draft_option_draftOptionNotFound(testfile_tex_no_draft_option,
                                                 config_dict):
    """Tests that the draft option from the classdefinition gets removed. """
    file_name = testfile_tex_no_draft_option
    # Collect lines in file
    with open(f"{file_name}.tex", "r") as f:
        lines_befor_runing_test: list[str] = [line.rstrip() for line in f]

    # run test function
    with pytest.raises(ValueError):
        underTest = operations.remove_draft_option(   # noqa: F841
            testfile_tex_no_draft_option,
            config_dict
        )

    with open(f"{file_name}.tex", "r") as f:
        lines_after_runing_test: list[str] = [line.rstrip() for line in f]

    assert lines_after_runing_test == lines_befor_runing_test


def test_create_bibliography(testfile_bib, config_dict):
    """ Tests the creation of a bibliography. """
    file_name = testfile_bib

    underTest = operations.create_bibliograpyh(file_name, config_dict)

    assert f"{file_name}.bbl" in os.listdir()


def test_create_bibliography_BcfFileNotFound(testfile_bib_no_bcf, config_dict):
    """ Tests the failure behaviour for the operation. """
    ...

