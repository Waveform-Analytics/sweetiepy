from datetime import datetime, timezone, timedelta


def parse_time_range(start_time: str = None, end_time: str = None):
    """
    Parse and validate the start_time and end_time inputs, defaulting to a two-week range.
    :param start_time: Start time as an ISO 8601 formatted string.
    :param end_time: End time as an ISO 8601 formatted string.
    :return: A tuple (start_time, end_time) as timezone-aware datetime objects.
    """
    if not end_time:
        end_time = datetime.now(timezone.utc)
    else:
        try:
            end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Invalid end_time format. Use ISO 8601 (e.g., 2023-10-01T12:34:56Z).")

    if not start_time:
        start_time = end_time - timedelta(weeks=2)
    else:
        try:
            start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Invalid start_time format. Use ISO 8601 (e.g., 2023-10-01T12:34:56Z).")

    if start_time >= end_time:
        raise ValueError("Start time must be earlier than end time.")

    return start_time, end_time


def normalize_timestamp(timestamp: str) -> datetime:
    """
    Normalize a timestamp to a timezone-aware UTC datetime object.
    :param timestamp: Timestamp string in ISO 8601 format.
    :return: A timezone-aware datetime object in UTC.
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            local_tz = datetime.now().astimezone().tzinfo
            dt = dt.replace(tzinfo=local_tz).astimezone(timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {timestamp}, error: {e}")
