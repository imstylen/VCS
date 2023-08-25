"""This module contains the main entry point for the application.

It sets up logging, defines the default paths for the application, and provides functions for creating the working folder and running the application.

Constants
---------
CURRENT_DIRECTORY : Path
    The directory containing this script. It's set to the parent of the current file's directory.
DEFAULT_WORKINGFOLDER_PATH : Path
    The default path where the application will create its working folder. It's set to a 'WorkingFolder' directory in the same directory as this script.

Functions
---------
get_home_relative_path() -> Path:
    Returns the home directory relative path.
create_working_folder(path: Path = None) -> Path:
    Creates a working folder at the given path. If no path is provided, uses the default working folder path.
main(app_path: Path | str = None) -> None:
    Starts the application, creates the working folder if it doesn't exist, and then closes the application.
"""
import logging
from pathlib import Path

from app import Application

logging.basicConfig(level=logging.INFO)

# Set the default path relative to the current script's directory, as to use the directory its contained within.
CURRENT_DIRECTORY = Path(__file__).parent.parent
DEFAULT_WORKINGFOLDER_PATH = CURRENT_DIRECTORY / 'WorkingFolder'


def get_home_relative_path() -> Path:
    """Returns the home directory relative path.

    Returns
    -------
    Path
        The home directory relative path.
    """
    return Path.home() / 'WorkingFolder'


def create_working_folder(path: Path = None) -> Path:
    """Creates a working folder at the given path. If no path is provided, uses the
    default working folder path.

    Parameters
    ----------
    path : Path, optional
        The path where to create the working folder (default is None).

    Returns
    -------
    Path
        The path of the created working folder.
    """
    if path is None:
        path = DEFAULT_WORKINGFOLDER_PATH
        logging.info("Using default path: %s", path)
    path.mkdir(exist_ok=True)
    return path


def main(app_path: Path | str = None) -> None:
    """Starts the application, creates the working folder if it doesn't exist. Then The
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
    # Creates the working folder if it doesn't exist, continues if it does.
    app_path = create_working_folder(app_path)
    application = Application(app_path)
    application.update()
    logging.info("Closing application")


if __name__ == "__main__":
    # This will use the script's relative path by default.
    main()

    # If you want to use the home directory relative path, you can call:
    # home_path = get_home_relative_path()
    # main(home_path)
