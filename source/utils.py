"""This module provides utility functions for handling timestamps.

Functions:
    get_current_time_str: Returns the current time as a string in the format "YYYY-MM-DD_HH-MM-SS".
    timestamp_string_to_unix_float: Converts a timestamp string to a Unix timestamp (seconds since the epoch).
"""
from datetime import datetime


def get_current_time_str() -> str:
    """Returns the current time as a string in the format "YYYY-MM-DD_HH-MM-SS".

    Returns
    -------
    str
        The current time as a string.
    """
    current_datetime = datetime.now()
    desired_format = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return desired_format


def timestamp_string_to_unix_float(timestamp_str: str) -> float:
    """Converts a timestamp string to a Unix timestamp (seconds since the epoch).

    Parameters
    ----------
    timestamp_str : str
        The timestamp string to convert.

    Returns
    -------
    float
        The Unix timestamp corresponding to the input string.
    """
    if not timestamp_str:
        return 0.0

    dt = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
    return dt.timestamp()
