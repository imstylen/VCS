"""This module contains the Application class which represents an application that
operates on a directory. It provides functionalities to process the directory and its
subdirectories, and handle files within them.

Classes:
    Application: Represents an application that operates on a directory.
"""
from pathlib import Path
from typing import Iterator

from source.file_handler import FileHandler


class Application:
    """A class used to represent an Application.

    Attributes
    ----------
    directory : Path
        The directory where the application operates.
    backup_folder : Path
        The backup folder for the application.
    file_handler : FileHandler
        The file handler for the application.

    Methods
    -------
    __repr__() -> str:
        Returns a string representation of the Application object.
    update() -> None:
        Updates the application by processing the directory.
    _setup_backup_folder() -> Path:
        Sets up the backup folder and returns its path.
    _process_directory(directory_path: Path, relative_path: Path = None) -> None:
        Processes the given directory and its subdirectories.
    get_directories(directory_path: Path) -> Iterator[Path]:
        Returns an iterator over the directories in the given path.
    get_files(directory_path: Path) -> Iterator[Path]:
        Returns an iterator over the files in the given path.
    """

    def __init__(self, in_directory: str) -> None:
        """Constructs all the necessary attributes for the Application object.

        Parameters
        ----------
        in_directory : str
            The directory where the application operates.
        """
        self.directory: Path = Path(in_directory)
        self.backup_folder: Path = self._setup_backup_folder()
        self.file_handler = FileHandler(self.backup_folder)

        self.update()

    def __repr__(self) -> str:
        """Returns a string representation of the Application object."""
        return f"Application({self.directory})"

    def update(self) -> None:
        """Updates the application by processing the directory."""
        self._process_directory(self.directory)

    def _setup_backup_folder(self) -> Path:
        """Sets up the backup folder and returns its path.

        Returns
        -------
        Path
            The path of the backup folder.
        """
        backup_folder: Path = self.directory / ".backup"
        backup_folder.mkdir(exist_ok=True)

        return backup_folder

    def _process_directory(self, directory_path: Path, relative_path: Path = None) -> None:
        """Processes the given directory and its subdirectories.

        Parameters
        ----------
        directory_path : Path
            The path of the directory to process.
        relative_path : Path, optional
            The relative path of the directory to process (default is None).
        """
        if relative_path is None:
            relative_path = Path()

        # Process directories first
        for path in self.get_directories(directory_path):
            new_relative_path = relative_path / path.name
            self._process_directory(path, new_relative_path)

        # Then process files
        for path in self.get_files(directory_path):
            self.file_handler.add_file(path, relative_path)

    @staticmethod
    def get_directories(directory_path: Path) -> Iterator[Path]:
        """Returns an iterator over the directories in the given path.

        Parameters
        ----------
        directory_path : Path
            The path to get directories from.

        Returns
        -------
        Iterator[Path]
            An iterator over the directories in the given path.
        """
        return (p for p in directory_path.iterdir() if p.is_dir() and p.name != ".backup")

    @staticmethod
    def get_files(directory_path: Path) -> Iterator[Path]:
        """Returns an iterator over the files in the given path.

        Parameters
        ----------
        directory_path : Path
            The path to get files from.

        Returns
        -------
        Iterator[Path]
            An iterator over the files in the given path.
        """
        return (p for p in directory_path.iterdir() if not p.is_dir())
