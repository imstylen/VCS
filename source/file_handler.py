import re
from pathlib import Path

from source.file import File
from source.utils import timestamp_string_to_unix_float


class FileHandler:
    def __init__(self, backup_folder: Path) -> None:
        self.backup_folder = backup_folder

    def get_latest_backup_time(self, file: File) -> str:
        backup_files = self.backup_folder.glob(f"{file.file_path.stem}_*{file.file_path.suffix}")

        pattern = r"_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})"
        timestamps = [re.search(pattern, str(f)).group(1) for f in backup_files if re.search(pattern, str(f))]

        return max(timestamps, default="")

    def needs_backup(self, file: File) -> bool:
        return file.last_updated > timestamp_string_to_unix_float(self.get_latest_backup_time(file))
