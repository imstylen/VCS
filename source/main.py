import logging
from pathlib import Path

from app import Application

DEFAULT_RELATIVE_PATH = 'WorkingFolder'
logging.basicConfig(level=logging.INFO)


def create_working_folder(path: Path | str = None) -> Path:
    if path is None:
        home_directory = Path.home()
        path = Path(home_directory / DEFAULT_RELATIVE_PATH)
    path.mkdir(exist_ok=True)
    return path


def main(app: Path | str = None) -> None:
    logging.info("Starting application")
    # Creates the working folder if it doesn't exist, continues if it does.
    app_path = create_working_folder(app)
    Application(app_path)
    logging.info("Closing application")


if __name__ == "__main__":
    home_directory = Path.home()
    target_directory = Path(home_directory / 'WorkingFolder')
    main(target_directory)
