from datetime import datetime

def format_duration(seconds):
    """
    Formats a duration in seconds into a human-readable string like '2h 15m' or '45s'.
    """
    if seconds is None or seconds < 0:
        return "0s"
        
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def get_timestamp():
    """
    Returns the current timestamp as a string formatted as YYYY-MM-DD HH:MM:SS.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date():
    """
    Returns the current date as a string formatted as YYYY-MM-DD.
    """
    return datetime.now().strftime("%Y-%m-%d")

def safe_divide(a, b, default=0.0):
    """
    Divides a by b safely, returning the default value if b is zero.
    """
    try:
        if b == 0:
            return default
        return a / b
    except (ZeroDivisionError, TypeError):
        return default

def clamp(value, min_val, max_val):
    """
    Restricts a value to be within the specified minimum and maximum bounds.
    """
    if value is None:
        return min_val
    return max(min_val, min(value, max_val))
