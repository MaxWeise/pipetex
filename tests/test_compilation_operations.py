""" Test the compile_latex, create_bibliograpyh and create_glossary functions.

@author Max Weise
created 26.07.2022
"""


from src.pipetex.operations import operations
from tests.shared_fixtures import testfile_tex, config_dict, testfile_bib, testfile_bib_no_bcf, testfile_glo   # noqa: E501

import os
import pytest

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


def test_create_bibliography(testfile_bib, config_dict):
    """ Tests the creation of a bibliography. """
    file_name = testfile_bib

    underTest = operations.create_bibliograpyh(file_name, config_dict)  # noqa: F841, E501

    assert f"{file_name}.bbl" in os.listdir()


def test_create_bibliography_BcfFileNotFound(testfile_bib_no_bcf, config_dict):
    """ Tests the failure behaviour for the operation. """
    with pytest.raises(FileNotFoundError):
        underTest = operations.create_bibliograpyh(     # noqa: F841
            testfile_bib_no_bcf,
            config_dict
        )


def test_create_glossaries(testfile_glo, config_dict):
    """Tests the creation of glossaries. """
    file_name = testfile_glo

    underTest = operations.create_glossary(file_name, config_dict)

    assert f"{file_name}.gls" in os.listdir()


def test_create_glossaries_AuxFileNotFoundError(testfile_glo, config_dict):
    """Tests if an error is raised when .aux file is missing. """
    file_name = testfile_glo
    with pytest.raises(FileNotFoundError):
        os.remove(f"{file_name}.aux")
        underTest = operations.create_glossary(
            testfile_glo,
            config_dict
        )


def test_create_glossaries_GloFileNotFoundError(testfile_glo, config_dict):
    """Tests if an error is raised when .glo file is missing. """
    file_name = testfile_glo
    with pytest.raises(FileNotFoundError):
        os.remove(f"{file_name}.glo")
        underTest = operations.create_glossary(
            testfile_glo,
            config_dict
        )


def test_create_glossaries_IstFileNotFoundError(testfile_glo, config_dict):
    """Tests if an error is raised when .ist file is missing. """
    file_name = testfile_glo
    with pytest.raises(FileNotFoundError):
        os.remove(f"{file_name}.ist")
        underTest = operations.create_glossary(
            testfile_glo,
            config_dict
        )


