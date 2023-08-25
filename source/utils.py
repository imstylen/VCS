from datetime import datetime


def get_current_time_str() -> str:
    current_datetime = datetime.now()
    desired_format = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return desired_format


def timestamp_string_to_unix_float(timestamp_str: str) -> float:
    if not timestamp_str:
        return 0.0

    dt = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
    return dt.timestamp()
