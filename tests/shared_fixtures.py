""" Pytest fixtures used when testing functions."""

# from tests.test_helpers.util_functions import remove_files
from tests.test_helpers import util_functions

import os
import pytest
import shutil


@pytest.fixture
def testfile_tex():
    test_file_name = "test_file"
    shutil.copy(f"./test_assets/tex_assets/{test_file_name}.tex", ".")
    yield test_file_name

    # remove texput.log specifically
    file_list = os.listdir()
    os.remove("texput.log") if "texput.log" in file_list else ...

    util_functions.remove_files(test_file_name)


@pytest.fixture
def testfile_tex_no_draft_option():
    test_file_name = "test_file_no_draft"
    shutil.copy(f"./test_assets/tex_assets/{test_file_name}.tex", ".")
    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def testfile_bib():
    test_file_name = "test_file_bib"
    shutil.copy(f"./test_assets/bib_assets/{test_file_name}.tex", ".")
    shutil.copy(f"./test_assets/bib_assets/{test_file_name}.bib", ".")
    shutil.copy(f"./test_assets/bib_assets/{test_file_name}.bcf", ".")
    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def testfile_bib_no_bcf():
    test_file_name = "test_file_bib"
    shutil.copy(f"./test_assets/bib_assets/{test_file_name}.tex", ".")
    shutil.copy(f"./test_assets/bib_assets/{test_file_name}.bib", ".")
    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def testfile_glo():
    test_file_name = "test_file_glo"
    shutil.copy(f"./test_assets/glo_assets/{test_file_name}.tex", ".")
    shutil.copy(f"./test_assets/glo_assets/{test_file_name}.ist", ".")
    shutil.copy(f"./test_assets/glo_assets/{test_file_name}.glo", ".")
    shutil.copy(f"./test_assets/glo_assets/{test_file_name}.aux", ".")
    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def testfile_glo_no_aux_files():
    test_file_name = "test_file_glo"
    shutil.copy(f"./test_assets/glo_assets/{test_file_name}.tex", ".")
    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def dirty_working_dir_files():
    """Creates a working directory filled with redundant aux files."""
    test_file_name = "test_file_glo"
    file_extentions: list[str] = ['tex', 'aux', 'pdf', 'glo', 'bib']
    for ex in file_extentions:
        with open(f"{test_file_name}.{ex}", 'x') as f:
            pass    # Empty file is sufficient

    yield test_file_name

    util_functions.remove_files(test_file_name)


@pytest.fixture
def config_dict():
    return {"file_prefix": "[piped]"}

