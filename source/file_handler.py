"""This module provides a FileHandler class for handling file backups.

The FileHandler class provides methods to check if a file needs backup,
perform the backup, and add new files to be managed by the handler.

Classes:
    FileHandler: Handles file backups.
"""
import logging
import re
import shutil
from pathlib import Path
from typing import Set

from source.file import File
from source.utils import get_current_time_str, timestamp_string_to_unix_float


class FileHandler:
    """A class used to handle files for backup purposes.

    Attributes
    ----------
    backup_folder : Path
        The folder where backups are stored.
    files : Set[File]
        The set of files handled by this handler.
    timestamp_pattern : Pattern
        The regex pattern used to match timestamps in filenames.

    Methods
    -------
    get_latest_backup_time(file: File) -> str:
        Returns the latest backup time for a given file.
    needs_backup(file: File) -> bool:
        Checks if a given file needs to be backed up.
    add_file(file_path: str | Path, relative_path: str) -> None:
        Adds a file to the handler and backs it up.
    backup(file: File, relative_path: str) -> None:
        Backs up a given file if necessary.
    """

    def __init__(self, backup_folder: Path) -> None:
        """Constructs all the necessary attributes for the FileHandler object.

        Parameters
        ----------
        backup_folder : Path
            The folder where backups are stored.
        """
        self.backup_folder = backup_folder
        self.files: Set[File] = set()
        self.timestamp_pattern = re.compile(r"_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})")

    def get_latest_backup_time(self, file: File) -> str:
        """Returns the latest backup time for a given file.

        Parameters
        ----------
        file : File
            The file to check for backups.

        Returns
        -------
        str
            The latest backup time as a string.
        """
        backup_files = self.backup_folder.glob(f"{file.file_path.stem}_*{file.file_path.suffix}")

        timestamps = []
        for file in backup_files:
            match = self.timestamp_pattern.search(str(file))
            if match:
                timestamps.append(match.group(1))

        return max(timestamps, default="")

    def needs_backup(self, file: File) -> bool:
        """Checks if a given file needs to be backed up.

        Parameters
        ----------
        file : File
            The file to check for backups.

        Returns
        -------
        bool
            True if the file needs to be backed up, False otherwise.
        """
        return file.last_updated > timestamp_string_to_unix_float(self.get_latest_backup_time(file))

    def add_file(self, file_path: str | Path, relative_path: str) -> None:
        """Adds a file to the handler and backs it up.

        Parameters
        ----------
        file_path : str | Path
            The path of the file to add.
        relative_path : str
            The relative path of the file to add.
        """
        file = File(file_path)
        self.files.add(file)
        self.backup(file, relative_path)

    def backup(self, file: File, relative_path: str) -> None:
        """Backs up a given file if necessary.

        Parameters
        ----------
        file : File
            The file to back up.
        relative_path : str
            The relative path of the file to back up.
        """
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
