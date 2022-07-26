""" Test file for the operations of the pipeline.

For now, all operations will be tested in this file. It is forseen though, that
the file will grow to a point where it is no longer practical and the
testcases need to be split into different files. How this will be done is not
entirely clear right now.

@author Max Weise
created 23.07.2022
"""

from src.pipetex.operations import operations
from tests.shared_fixtures import testfile_tex, config_dict, testfile_tex_no_draft_option   # noqa: E501

import os
import pytest

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


