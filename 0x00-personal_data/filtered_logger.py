#!/usr/bin/env python3
"""
Implement a custom log record formatter that redacts sensitive information.
"""

import re
import os
import logging
from typing import List
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns the log message obfuscated.

    Args:
        fields (list): the fields to obfuscate in the log message
        redaction (str): the obfuscated text to replace the field value
        message (str): the log message
        separator (str): the separator for the log message
    """
    for field in fields:
        message = re.sub(
            field + '=.+?' + separator,
            field + '=' + redaction + separator,
            message,
        )
    return message


# Define PII_FIELDS constant
PII_FIELDS = ("name", "email", "phone", "password", "ssn")


def get_logger() -> logging.Logger:
    """Creates and returns a logger configured for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # Create FileHandler
    file_handler = logging.FileHandler("user_data.log")
    file_handler.setLevel(logging.INFO)
    # Create StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))  # type: ignore
    stream_handler.setLevel(logging.INFO)
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.MySQLConnection:
    """
    Returns a connection to a MySQL DB using credentials from the env variables
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db = os.getenv('PERSONAL_DATA_DB_NAME', "my_db")
    conn = mysql.connector.connect(
        user=user, password=password, host=host, database=db
    )
    return conn  # type: ignore


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the RedactingFormatter object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record):
        """Format the log record."""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def main():
    """Main function"""

    hash_password = __import__('encrypt_password').hash_password

    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names if cursor.column_names else []
    for row in cursor.fetchall():
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
