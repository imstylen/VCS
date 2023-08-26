"""This module provides a File class for handling file-related operations.

The File class provides methods to get the string representation of the file and
to get the last updated time of the file.

Classes:
    File: Represents a file, handling Path related logic, as well as the history on when it was last updated.
"""
from pathlib import Path


class File:
    """A class used to represent a File.

    Attributes
    ----------
    file_path : Path
        The path of the file.

    Methods
    -------
    __str__() -> str:
        Returns a string representation of the File object.
    last_updated() -> float:
        Returns the last updated time of the file in seconds since the epoch as a floating point number.
    """

    def __init__(self, file_path: str | Path) -> None:
        """Constructs the File object.

        Parameters
        ----------
        file_path : str | Path
            The path of the file.
        """
        self.file_path: Path = Path(file_path)

    def __str__(self) -> str:
        """Returns a string representation of the File object."""
        return str(self.file_path)

    @property
    def last_updated(self) -> float:
        """Returns the last updated time of the file in seconds since the epoch as a
        floating point number.

        Returns
        -------
        float
            The last updated time of the file.
        """
        return self.file_path.stat().st_mtime
