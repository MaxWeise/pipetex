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
from typing import Any


@pytest.fixture
def testfile_tex():
    test_file_name = "test_file"
    shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
    yield test_file_name

    remove_files(test_file_name)
    # remove texput.log specifically
    os.remove("texput.log")



# @pytest.fixture
# def testfile_glo():
#     test_file_name = "test_file_glo"
#     shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
#     yield test_file_name
#     remove_files(test_file_name)


# @pytest.fixture
# def testfile_bib():
#     test_file_name = "test_file_bib"
#     shutil.copy(f"./test_assets/{test_file_name}.tex", ".")
#     shutil.copy(f"./test_assets/{test_file_name}.bib", ".")
#     yield test_file_name
#     remove_files(test_file_name)


@pytest.fixture
def config_dict():
    return {}


def test_compile_latex_file(testfile_tex, config_dict):
    """Tests the compilation of latex files. """
    # Setup Code
    file_name = testfile_tex

    # run test function
    underTest = operations.compile_latex_file(file_name, config_dict)

    # assert statements
    assert f"{file_name}.pdf" in os.listdir("."), (
            f"The file {file_name}.pdf does not exist"
    )
    assert os.stat(f"{file_name}.pdf").st_size > 0


def test_compile_latex_file_fileNotFound(config_dict):
    """Tests the compilation of latex files. """
    # run test function
    with pytest.raises(FileNotFoundError):
        underTest = operations.compile_latex_file("not_a_file", config_dict)

