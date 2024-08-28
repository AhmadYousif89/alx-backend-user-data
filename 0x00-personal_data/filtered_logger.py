#!/usr/bin/env python3
"""
Implement a custom log record formatter that redacts sensitive information.
"""

import logging
from typing import List
import re

def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    """
    Given a log message, obfuscate the sensitive information.

    Args:
    - fields (str): A string of fields to redact.
    - redaction (str):
        A string representing what the sensitive data will be replaced with.
    - msg (str): The log message.
    - sep (str):
        A string representing by which character the fields are separated.

    Returns:
    - A new string with the sensitive data redacted.
    """
    for field in fields:
        msg = re.sub(fr"{field}=.+?{sep}", f"{field}={redaction}{sep}", msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        """Initialize the RedactingFormatter object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        
    def format(self, record):
        """Format the log record."""
        return filter_datum(
            [self.FORMAT], self.REDACTION,
            super().format(record), self.SEPARATOR
        )
