"""Main script for the pipeline application.

This file provides a CLI to the user and executes the pipeline with the
specified parameters. It is not responsible for any errorhandling which occur
while running the pipeline.

@author: Max Weise
created: 11.08.2022
"""

def _setup_sysarg_parser():
    """Creates a namespace which contains the arguments passed by the user."""

    # File Name, pos, str
    # Create bib, opt, bool, False
    # Create glo, opt, bool, False
    # quiet, opt, bool, False | Changes log level to warning
    # verbose, opt, bool, False | Prints output of pdflate, biber, ... to strout
    return None


def _setup_logger():
    """Creates the logger instanc(es) for the script."""

    # TODO: use coloredlogs
    # Create a stream handler
    #   lvl: info or warning depending on user settings, name: pipetex,
    # Create a file handler
    #   lvl: DEBUG, name: pipetex

    return None


def main():
    """Main method of the module."""
    ...


if __name__ == "__main__":
    main()

