#!/usr/bin/env python3
""" Filtering log """
import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Return an obfuscated log message
    """
    for field in fields:
        message = re.sub(
            field + "=.+?" + separator,
            field + "=" + redaction + separator, message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formating the log message '''

        # Let's first get the default --log message formatting-- provided
        # + by the ----logging module----
        log_message = super().format(record)

        # Then using filter_datum function we reformat the message
        log_message = filter_datum(
            self.fields, self.REDACTION, log_message, self.SEPARATOR
        )
        return log_message


def get_logger() -> logging.Logger:
    ''' Creating logger object and customize it '''
    # Create a logger named "user_data"
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)  # Limit the log level to INFO

    # Prevent messages from propagating to other loggers
    logger.propagate = False

    # Create a StreamHandler with RedactingFormatter as formatter
    stream_handler = StreamHandler()
    redacting_formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(redacting_formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger
