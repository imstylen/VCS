from pathlib import Path


class File:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path: Path = Path(file_path)

    def __str__(self) -> str:
        return str(self.file_path)

    @property
    def last_updated(self) -> float:
        return self.file_path.stat().st_mtime
