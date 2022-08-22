""" Test the functionality of the pipeline class.

@author Max Weise
created 29.07.2022
"""

from src.pipetex.pipeline import Pipeline
from src.pipetex.enums import ConfigDictKeys
from tests import util_functions

import os
import pytest
import shutil


# === Fixtures ===
@pytest.fixture
def simple_test_environment():
    """Generates a tex file which includes bibliography and glossary"""
    test_file = "test_file"
    with open(f"{test_file}.tex", "w+", encoding="utf-8") as f:
        f.write(
            "\\documentclass[a4paper, 12pt, draft]{scrreprt}\n"
            "\\usepackage{biblatex}\n"
            "\\usepackage{glossaries}\n"
            "\\makeglossaries\n"
            "\\addbibresource{" + test_file + ".bib}\n"
            "\\newglossaryentry{Werksexperten}"
            "{name={Werksexperte}, description={Beschreibung}}\n"
            "\\begin{document}\n"
            "This is a Tex file \\\\ I hope this is in a new line\n"
            "This is a test entrie \\Gls{Werksexperten}"
            "Source \\cite{test}\n"
            "\\printbibliography\n"
            "\\end{document}"
        )

        with open(f'{test_file}.bib', 'w+', encoding='utf-8') as f:
            f.write(
                '@misc{test,\n'
                'author  = {BSI},\n'
                'year    = {},\n'
                'title   = {Spielregeln für digitale Sicherheit}\n'
                '}'
            )

    yield test_file

    if "DEPLOY" in os.listdir():
        shutil.rmtree("DEPLOY")

    util_functions.remove_files(test_file)


@pytest.fixture
def simple_test_environment_no_draft():
    """Generates a tex file which includes bibliography and glossary

    This is a simple workaround as mocking functions currently does not work.
    """
    test_file = "test_file"
    with open(f"{test_file}.tex", "w+", encoding="utf-8") as f:
        f.write(
            "\\documentclass[a4paper, 12pt]{scrreprt}\n"
            "\\usepackage{biblatex}\n"
            "\\usepackage{glossaries}\n"
            "\\makeglossaries\n"
            "\\addbibresource{" + test_file + ".bib}\n"
            "\\newglossaryentry{Werksexperten}"
            "{name={Werksexperte}, description={Beschreibung}}\n"
            "\\begin{document}\n"
            "This is a Tex file \\\\ I hope this is in a new line\n"
            "This is a test entrie \\Gls{Werksexperten}"
            "Source \\cite{test}\n"
            "\\printbibliography\n"
            "\\end{document}"
        )

        with open(f'{test_file}.bib', 'w+', encoding='utf-8') as f:
            f.write(
                '@misc{test,\n'
                'author  = {BSI},\n'
                'year    = {},\n'
                'title   = {Spielregeln für digitale Sicherheit}\n'
                '}'
            )

    yield test_file

    if "DEPLOY" in os.listdir():
        shutil.rmtree("DEPLOY")

    util_functions.remove_files(test_file)


@pytest.fixture
def config_dict():
    return {"file_prefix": "[piped]", "new_name": "[piped]_test_file"}


def test_pipeline_init():
    """Tests that the pipeline is initialized correctly."""
    file_name = "test_file_for_init"

    underTest = Pipeline(file_name, create_bib=True)

    assert underTest.order_of_operations
    assert len(underTest.order_of_operations) == 6


def test_execution(simple_test_environment, config_dict):
    """Tests the correct execution of the pipeline."""
    file_name = simple_test_environment

    underTest = Pipeline(file_name, create_bib=True, create_glo=True)

    rv, ex = underTest.execute(file_name)

    assert rv
    assert not ex

    files_in_working_dir = os.listdir()

    assert "DEPLOY" in files_in_working_dir

    files_in_dir = os.listdir("./DEPLOY")

    local_file_name = config_dict[ConfigDictKeys.NEW_NAME.value]
    assert f"{local_file_name}.pdf" in files_in_dir


def test_execution_E_low_severityLevel(simple_test_environment_no_draft,
                                       config_dict):
    """Test execution in case of failure.

    When a low severity_level is detected, the pipeline should make some sort
    of logging statemet and continue with the execution.
    TODO: Research hot to test logging with pytest
    """
    test_file = simple_test_environment_no_draft
    underTest = Pipeline(test_file, config_dict)

    success, error = underTest.execute(test_file)

    assert success
    assert error
    assert error.severity_level <= 10


def test_execution_E_high_severityLevel(simple_test_environment, config_dict):
    """Test execution in case of failure.

    When a high severity_level is detected, the pipeline should make some sort
    of logging statemet and continue with the execution. This level is used
    when optional features of the pipeline fail but a pdf file can still be
    created.
    TODO: Research hot to test logging with pytest
    """
    test_file = simple_test_environment
    underTest = Pipeline(test_file, create_bib=True)
    os.remove(f"{test_file}.bib")

    success, error = underTest.execute(test_file)

    assert not success
    assert error
    assert 10 < error.severity_level <= 20


def test_execution_E_critical_severityLevel():
    """Test execution in case of failure.

    When a critical severity_level is detected, the pipeline should make some
    sort of logging statemet and aboart the execution. This level is used when
    core features of the pipeline fail or a tex file can not be found.
    TODO: Research hot to test logging with pytest
    """
    test_file = "not_a_testfile"
    underTest = Pipeline(test_file)

    success, error = underTest.execute(test_file)

    assert not success
    assert error
    assert 20 < error.severity_level <= 30

