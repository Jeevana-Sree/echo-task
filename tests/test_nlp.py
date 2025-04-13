import pytest
from app.nlp import extract_task_and_time
from datetime import datetime

def test_extract_valid_task():
    text = "Remind me to submit assignment at 6 PM"
    task, task_time = extract_task_and_time(text)
    assert task == "submit assignment"
    assert isinstance(task_time, datetime)

def test_extract_invalid_format():
    text = "Don't remind me"
    task, task_time = extract_task_and_time(text)
    assert task is None
    assert task_time is None

def test_extract_tomorrow_time():
    text = "Remind me to walk dog tomorrow at 7 AM"
    task, task_time = extract_task_and_time(text)
    assert task == "walk dog tomorrow"
    assert isinstance(task_time, datetime)
