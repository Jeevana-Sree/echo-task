import re
import dateparser
from datetime import datetime

def extract_task_and_time(text):
    """
    Extracts task and time from a command like:
    "Remind me to call mom at 5 PM"
    Returns:
        task (str): The task description
        task_time (datetime): Parsed datetime object
    """
    match = re.search(r"remind me to (.+?) at (.+)", text, re.IGNORECASE)
    if match:
        task = match.group(1).strip()
        time_str = match.group(2).strip()
        task_time = dateparser.parse(time_str)
        return task, task_time
    return None, None
