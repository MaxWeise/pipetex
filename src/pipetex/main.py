"""Main script for the pipeline application.

This file provides a CLI to the user and executes the pipeline with the
specified parameters. It is not responsible for any errorhandling which occur
while running the pipeline.

@author: Max Weise
created: 11.08.2022
"""

import pipeline

import argparse
import coloredlogs
import logging


def _setup_sysarg_parser() -> argparse.Namespace:
    """Creates a namespace which contains the arguments passed by the user.

    Define CLI arguments in this function.

    Returns:
        parser: Namespace holding all CLI arguments.

    """
    parser = argparse.ArgumentParser()

    # === Positional Arguments ===
    parser.add_argument(
        "filename",
        help="Name of file which is processed by the pipeline."
    )

    # === Optional Arguments and Flags ===
    # parser.add_argument(  # TODO: Implement later
    #     "-v",
    #     help="Turn on console output for the latex engines.",
    #     action="store_true"
    # )

    parser.add_argument(
        "-q",
        help="Turn the termil log level down to WARNING",
        action="store_true"
    )

    parser.add_argument(
        "-b", "--bib",
        help="Create a bibliography in the current latex project",
        action="store_true"
    )

    parser.add_argument(
        "-g", "--gls",
        help="Create a glossary in the current latex project",
        action="store_true"
    )


    # verbose, opt, bool, False | Prints output of pdflate, biber, ... to strout
    return parser.parse_args()


# TODO: Add return typehint
def _setup_logger(is_quiet: bool = False,
                  log_file_path: str = "log_file.txt"):
    """Creates the logger instanc(es) for the script.

    Args:
        is_quiet: When specified, the log level of the console handler will
            be set to WARNING. Defaults to False.
        log_file_path: Path to the logfile where the FileHandler writes the
            logs to. If no extra path is given, log_file.txt is used.

    Returns:
        logger: Logger object which has a Console- and FileHandler
            added to it.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    frmt = logging.Formatter(
        '[%(name)s - %(levelname)s] - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(
            logging.WARNING if is_quiet else logging.DEBUG
    )
    console_handler.setFormatter(frmt)

    # TODO: Create logfiles in seperate folder
    #       Each run of the pipeline should create a seperate log file
    #       (maybe limit this number to ~10 files in the folder)
    #       Include a header for each logfile containing metadata
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(frmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def main():
    """Main method of the module."""
    cli_args = _setup_sysarg_parser()
    logger = _setup_logger()

    p = pipeline.Pipeline(
        cli_args.filename,
        create_bib=cli_args.bib,
        create_glo=cli_args.gls,
        # TODO: Implement verbose option in pipeline object
        # verbose=cli.v,
        quiet=cli_args.q
    )

    p.execute(p.file_name)


if __name__ == "__main__":
    main()
