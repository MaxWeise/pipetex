""" Test the compile_latex, create_bibliograpyh and create_glossary functions.

@author Max Weise
created 26.07.2022
"""


from src.pipetex.operations import operations
from src.pipetex.utils import exceptions

from tests import util_functions

import os
import pytest

from typing import Optional, Tuple


# === Fixtures ===
@pytest.fixture
def simple_testfile():
    """A test file to test the compilation of latex files."""
    file_name: str = "test_file"
    ex = ["tex"]
    util_functions.write_empty_file(file_name, ex)

    yield file_name

    util_functions.remove_files(file_name)


@pytest.fixture
def bibliography_testfile():
    """A test file to test the creation of a bibliography in latex."""
    file_name = "test_file"
    ex = ["tex", "bib", "bcf"]
    util_functions.write_empty_file(file_name, ex)

    yield file_name

    util_functions.remove_files(file_name)


@pytest.fixture
def glossary_testfile():
    """A test file to test the creation of a glossary in latex."""
    file_name = "test_file"
    ex = ["tex", "aux", "glo", "ist"]
    util_functions.write_empty_file(file_name, ex)

    yield file_name

    util_functions.remove_files(file_name)


@pytest.fixture
def config_dict():
    return {
        "file_prefix": "[piped]",
        "verbose": False
    }


# === Type Def ===
Monad = Tuple[bool, Optional[exceptions.InternalException]]


# === Test Functions ===
def test_compile_latex_file(simple_testfile, config_dict, mocker):
    """Tests the compilation of latex files. """
    # Setup Code
    file_name = simple_testfile

    # run test function
    mocker.patch("subprocess.call", return_value=None)
    succsess, error = operations.compile_latex_file(file_name, config_dict)

    # assert statements
    assert succsess
    assert not error


def test_compile_latex_file_fileNotFound(config_dict):
    """Tests that the compilation function raises an appropriate error. """
    # run test function
    succsess, error = operations.compile_latex_file("not_a_file", config_dict)

    assert not succsess
    assert error
    assert 20 < error.severity_level <= 30
    assert type(error.severity_level) == int


def test_create_bibliography(bibliography_testfile, config_dict, mocker):
    """ Tests the creation of a bibliography. """
    file_name = bibliography_testfile

    mocker.patch("subprocess.call", return_value=None)
    succsess, error = operations.create_bibliograpyh(file_name, config_dict)

    assert succsess
    assert not error


def test_create_bibliography_BcfFileNotFound(config_dict, mocker):
    """ Tests the failure behaviour for the operation. """
    # Setting up test env
    file_name = "not_a_testfile"

    mocker.patch("subprocess.call", return_value=None)
    succsess, error = operations.create_bibliograpyh(file_name, config_dict)

    assert not succsess
    assert error
    assert 10 < error.severity_level <= 20
    assert type(error.severity_level) == int


def test_create_bibliography_BibFileNotFound(bibliography_testfile,
                                             config_dict, mocker):
    """Test the correct behaviour when no bib file was found."""
    file_name = bibliography_testfile
    os.remove(f"{file_name}.bib")

    succsess, error = operations.create_bibliograpyh(file_name, config_dict)

    assert not succsess
    assert error
    assert 10 < error.severity_level <= 20
    assert type(error.severity_level) == int


def test_create_glossaries(glossary_testfile, config_dict, mocker):
    """Tests the creation of glossaries. """
    file_name = glossary_testfile

    mocker.patch("subprocess.call", return_value=None)
    succsess, error = operations.create_glossary(file_name, config_dict)

    assert succsess
    assert not error


def test_create_glossaries_AuxFileNotFoundError(config_dict, mocker):
    """Tests if an error is raised when .aux file is missing. """
    file_name = "no_valid_testfile"
    succsess, error = operations.create_glossary(file_name, config_dict)

    assert not succsess
    assert 10 < error.severity_level <= 20
    assert type(error.severity_level) == int


def test_create_glossaries_GloFileNotFoundError(config_dict, mocker):
    """Tests if an error is raised when .glo file is missing. """
    file_name = "no_valid_testfile"
    succsess, error = operations.create_glossary(file_name, config_dict)

    assert not succsess
    assert 10 < error.severity_level <= 20
    assert type(error.severity_level) == int


def test_create_glossaries_IstFileNotFoundError(config_dict, mocker):
    """Tests if an error is raised when .ist file is missing. """
    file_name = "no_valid_testfile"
    succsess, error = operations.create_glossary(file_name, config_dict)

    assert not succsess
    assert 10 < error.severity_level <= 20
    assert type(error.severity_level) == int

