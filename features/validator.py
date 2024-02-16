import re
from datetime import datetime

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_text(text):
    if not isinstance(text, str) or len(text) > 20:
        return False

    if not re.match("^[a-zA-Z_]*$", text):
        return False

    return True

def is_valid_bsc_address(text):
    if not isinstance(text, str) or len(text) != 43:
        return False

    if not re.match("^=0x[a-zA-Z0-9]*$", text):
        return False

    return True