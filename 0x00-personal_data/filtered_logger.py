#!/usr/bin/env python3
""" Filtering log """
import re
from typing import List
import logging


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
        log_message = super().format(record)
        log_message = filter_datum(
            self.fields, self.REDACTION, log_message, self.SEPARATOR
        )
        return log_message
