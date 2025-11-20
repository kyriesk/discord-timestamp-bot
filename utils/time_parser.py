"""
Time parsing utilities for converting natural language and relative time 
to Discord timestamps.
"""
import re
from datetime import datetime, timedelta
import dateparser
import pytz


def parse_natural_time(time_str: str, user_timezone: str = "UTC") -> datetime:
    """
    Parse natural language time strings like "today 3pm", "tomorrow", "next friday".
    
    Args:
        time_str: Natural language time string
        user_timezone: User's timezone (IANA format, e.g., "America/New_York")
    
    Returns:
        datetime object in the user's timezone
    
    Raises:
        ValueError: If the time string cannot be parsed
    """
    try:
        tz = pytz.timezone(user_timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Unknown timezone: {user_timezone}")
    
    # Use dateparser with timezone settings
    settings = {
        'TIMEZONE': user_timezone,
        'RETURN_AS_TIMEZONE_AWARE': True,
        'PREFER_DATES_FROM': 'future'
    }
    
    parsed_dt = dateparser.parse(time_str, settings=settings)
    
    if parsed_dt is None:
        raise ValueError(f"Could not parse time string: {time_str}")
    
    return parsed_dt


def parse_relative_time(duration_str: str) -> datetime:
    """
    Parse relative time strings like "1 hour", "30 minutes", "2 hours 15 minutes".
    
    Args:
        duration_str: Relative time string
    
    Returns:
        datetime object representing the future time
    
    Raises:
        ValueError: If the duration string cannot be parsed
    """
    now = datetime.now(pytz.UTC)
    
    # Normalize the string
    duration_str = duration_str.lower().strip()
    
    # Parse hours and minutes
    hours = 0
    minutes = 0
    
    # Pattern for "X hour(s) Y minute(s)"
    hour_pattern = r'(\d+)\s*(?:hour|hr|h)s?'
    minute_pattern = r'(\d+)\s*(?:minute|min|m)s?'
    
    hour_match = re.search(hour_pattern, duration_str)
    minute_match = re.search(minute_pattern, duration_str)
    
    if hour_match:
        hours = int(hour_match.group(1))
    
    if minute_match:
        minutes = int(minute_match.group(1))
    
    if hours == 0 and minutes == 0:
        raise ValueError(f"Could not parse duration: {duration_str}")
    
    delta = timedelta(hours=hours, minutes=minutes)
    return now + delta


def generate_discord_timestamp(dt: datetime, format_type: str = "F") -> str:
    """
    Generate a Discord timestamp string from a datetime object.
    
    Args:
        dt: datetime object
        format_type: Discord timestamp format
            - "t": Short Time (e.g., 9:41 PM)
            - "T": Long Time (e.g., 9:41:30 PM)
            - "d": Short Date (e.g., 30/06/2021)
            - "D": Long Date (e.g., 30 June 2021)
            - "f": Short Date/Time (default) (e.g., 30 June 2021 9:41 PM)
            - "F": Long Date/Time (e.g., Wednesday, 30 June 2021 9:41 PM)
            - "R": Relative Time (e.g., 2 months ago)
    
    Returns:
        Discord timestamp string
    """
    timestamp = int(dt.timestamp())
    return f"<t:{timestamp}:{format_type}>"


def get_all_format_examples(dt: datetime) -> dict:
    """
    Get all Discord timestamp format examples for a given datetime.
    
    Args:
        dt: datetime object
    
    Returns:
        Dictionary mapping format names to timestamp strings
    """
    formats = {
        "Short Time": ("t", generate_discord_timestamp(dt, "t")),
        "Long Time": ("T", generate_discord_timestamp(dt, "T")),
        "Short Date": ("d", generate_discord_timestamp(dt, "d")),
        "Long Date": ("D", generate_discord_timestamp(dt, "D")),
        "Short Date/Time": ("f", generate_discord_timestamp(dt, "f")),
        "Long Date/Time": ("F", generate_discord_timestamp(dt, "F")),
        "Relative": ("R", generate_discord_timestamp(dt, "R"))
    }
    return formats
