import logging
from pathlib import Path

from app import Application

logging.basicConfig(level=logging.INFO)

# Set the default path relative to the current script's directory, as to use the directory its contained within.
CURRENT_DIRECTORY = Path(__file__).parent.parent
DEFAULT_WORKINGFOLDER_PATH = CURRENT_DIRECTORY / 'WorkingFolder'


def get_home_relative_path() -> Path:
    return Path.home() / 'WorkingFolder'


def create_working_folder(path: Path = None) -> Path:
    if path is None:
        path = DEFAULT_WORKINGFOLDER_PATH
        logging.info("Using default path: %s", path)
    path.mkdir(exist_ok=True)
    return path


def main(app_path: Path | str = None) -> None:
    logging.info("Starting application")
    app_path = Path(app_path) if app_path else None
    # Creates the working folder if it doesn't exist, continues if it does.
    app_path = create_working_folder(app_path)
    Application(app_path)
    logging.info("Closing application")


if __name__ == "__main__":
    # This will use the script's relative path by default.
    main()

    # If you want to use the home directory relative path, you can call:
    # home_path = get_home_relative_path()
    # main(home_path)
