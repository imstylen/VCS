from pathlib import Path
from typing import Iterator

from source.file_handler import FileHandler


class Application:
    def __init__(self, in_directory: str) -> None:
        self.directory: Path = Path(in_directory)
        self.backup_folder: Path = self._setup_backup_folder()
        self.file_handler = FileHandler(self.backup_folder)

        self.update()

    def __repr__(self) -> str:
        return f"Application({self.directory})"

    def update(self) -> None:
        self._process_directory(self.directory)

    def _setup_backup_folder(self) -> Path:
        backup_folder: Path = self.directory / ".backup"
        backup_folder.mkdir(exist_ok=True)

        return backup_folder

    def _process_directory(self, directory_path: Path, relative_path: Path = None) -> None:
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
        return (p for p in directory_path.iterdir() if p.is_dir() and p.name != ".backup")

    @staticmethod
    def get_files(directory_path: Path) -> Iterator[Path]:
        return (p for p in directory_path.iterdir() if not p.is_dir())
