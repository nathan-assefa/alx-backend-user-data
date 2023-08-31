#!/usr/bin/env python3
""" Filtering log """
import re
from typing import List
import logging
import os
import mysql.connector


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
    # First let's create a logger instance named "user_data"
    logger = logging.getLogger("user_data")

    # Then we need to limit severity level(order of importance)
    logger.setLevel(logging.INFO)

    # Prevent messages from propagating to other loggers(parent or child)
    logger.propagate = False

    # Create a StreamHandler with RedactingFormatter as formatter
    # This is what sends the log to the screen
    stream_handler = logging.StreamHandler()

    # parameterizing the formmater
    redacting_formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(redacting_formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' Getting values of envionment varibales using os module getenv '''
    db_username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name: str = os.getenv("PERSONAL_DATA_DB_NAME")

    # Create a connection to the database using mysql.connector
    db_connection = mysql.connector.connection.MySQLConnection(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )
    return db_connection


def main():
    """
    main entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
