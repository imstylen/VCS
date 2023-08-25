import logging
import shutil
from pathlib import Path

from file import File
from source.file_handler import FileHandler
from utils import get_current_time_str


class Application:
    def __init__(self, in_directory: str) -> None:
        self.directory: Path = Path(in_directory)
        self.backup_folder: Path = self.setup_backup_folder()
        self.file_handler = FileHandler(self.backup_folder)

        self.files: set[File] = set()
        self.update()

    def setup_backup_folder(self) -> Path:
        backup_folder: Path = self.directory / ".backup"
        backup_folder.mkdir(exist_ok=True)

        return backup_folder

    def add_file(self, file_path: str | Path) -> None:
        file = File(file_path)
        self.files.add(file)
        self.backup(file)

    def update(self) -> None:
        for directory_path in self.directory.iterdir():
            if directory_path.is_dir():
                logging.info("Skipping directory: %s", directory_path.name)
                continue

            if File(directory_path) not in self.files:
                self.add_file(directory_path)
            else:
                logging.info("Found: %s... Skipping", directory_path.name)

    def backup(self, file: File) -> None:
        if self.file_handler.needs_backup(file):
            logging.info("Backing up: %s", file.file_path)
            time_string = get_current_time_str()
            logging.info("Current time string: %s", time_string)
            backup_path = self.backup_folder / f"{file.file_path.stem}_{time_string}{file.file_path.suffix}"
            logging.info(backup_path)
            try:
                shutil.copy(file.file_path, backup_path)
                logging.info("Backup successful: %s", backup_path)
            except FileNotFoundError:
                logging.error("File not found: %s", file.file_path)
            except PermissionError:
                logging.error("Permission denied: %s", file.file_path)
            except IOError:
                logging.error("IO error occurred while backing up: %s", file.file_path)
        else:
            logging.info("No changes in: %s. Skipping backup.", file.file_path)
