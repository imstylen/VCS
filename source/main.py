"""This module contains the main entry point for the application.

It sets up logging, defines the default paths for the application, and provides functions for creating the VcsDirectory and running the application.

Constants
---------
CURRENT_DIRECTORY : Path
    The directory containing this script. It's set to the parent of the current file's directory.
DEFAULT_VCS_DIR_PATH : Path
    The default path where the application will create its VcsDirectory. It's set to a 'VcsDirectory' directory in the same directory as this script.

Functions
---------
get_home_relative_path() -> Path:
    Returns the home directory relative path.
create_vcs_root_directory(path: Path = None) -> Path:
    Creates a VcsDirectory at the given path. If no path is provided, uses the default VcsDirectory path.
main(app_path: Path | str = None) -> None:
    Starts the application, creates the VcsDirectory if it doesn't exist, and then closes the application.
"""
import argparse
import logging
from pathlib import Path

from app import Application

# Set the default path relative to the current script's directory, as to use the directory its contained within.
CURRENT_DIRECTORY = Path(__file__).parent.parent
DEFAULT_VCS_FOLDER_NAME = 'VcsDirectory'
DEFAULT_VCS_DIR_PATH = CURRENT_DIRECTORY / DEFAULT_VCS_FOLDER_NAME
DEFAULT_LOG_LEVEL = logging.INFO


def get_home_relative_path(folder_name: str = None) -> Path:
    """Returns the home directory relative path.

    Returns
    -------
    Path
        The home directory relative path.
    """
    if folder_name is None:
        folder_name = DEFAULT_VCS_FOLDER_NAME
    return Path.home() / folder_name


def create_vcs_root_directory(path: Path = None) -> Path:
    """Creates a VcsDirectory at the given path. If no path is provided, uses the
    default VcsDirectory path.

    Parameters
    ----------
    path : Path, optional
        The path where to create the VcsDirectory (default is None).

    Returns
    -------
    Path
        The path of the created VcsDirectory.
    """
    if path is None:
        path = DEFAULT_VCS_DIR_PATH
        logging.info("Using default path: %s", path)
    path.mkdir(exist_ok=True)
    return path


def main(app_path: Path | str = None) -> None:
    """Starts the application, creates the backup folder if it doesn't exist. Then the
    application creates copies of files following the same directory structure within a
    .backup folder. Each copy is timestamped and appended to the end of the original
    filename in the format %Y-%m-%d_%H-%M-%S.

    Parameters
    ----------
    app_path : Path | str, optional
        The path of the application (default is None).
    """
    logging.info("Starting application")
    app_path = Path(app_path) if app_path else None
    # Creates the VcsDirectory if it doesn't exist, continues if it does.
    app_path = create_vcs_root_directory(app_path)
    application = Application(app_path)
    application.update()
    logging.info("Closing application")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the application.')
    # Use . for the current directory the CLI is run from
    parser.add_argument('--path', type=str, default=DEFAULT_VCS_DIR_PATH, help="The path of the working directory or 'script' for script directory")
    parser.add_argument('--log', type=str, default=DEFAULT_LOG_LEVEL, help='Set the log level')
    args = parser.parse_args()

    log_level = logging.getLevelName(args.log)
    logging.basicConfig(level=log_level)

    path = args.path
    main(path)
