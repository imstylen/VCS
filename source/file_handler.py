import logging
import re
import shutil
from pathlib import Path
from typing import Set

from source.file import File
from source.utils import get_current_time_str, timestamp_string_to_unix_float


class FileHandler:
    def __init__(self, backup_folder: Path) -> None:
        self.backup_folder = backup_folder
        self.files: Set[File] = set()
        self.timestamp_pattern = re.compile(r"_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})")

    def get_latest_backup_time(self, file: File) -> str:
        backup_files = self.backup_folder.glob(f"{file.file_path.stem}_*{file.file_path.suffix}")

        timestamps = []
        for file in backup_files:
            match = self.timestamp_pattern.search(str(file))
            if match:
                timestamps.append(match.group(1))

        return max(timestamps, default="")

    def needs_backup(self, file: File) -> bool:
        return file.last_updated > timestamp_string_to_unix_float(self.get_latest_backup_time(file))

    def add_file(self, file_path: str | Path, relative_path: str) -> None:
        file = File(file_path)
        self.files.add(file)
        self.backup(file, relative_path)

    def backup(self, file: File, relative_path: str) -> None:
        if self.needs_backup(file):
            time_string = get_current_time_str()
            logging.info("Backing up: %s", file.file_path)
            logging.info("Current time string: %s", time_string)
            backup_path = self.backup_folder / relative_path / f"{file.file_path.stem}_{time_string}{file.file_path.suffix}"
            backup_path.parent.mkdir(parents=True, exist_ok=True)
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
