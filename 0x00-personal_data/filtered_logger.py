#!/usr/bin/env python3
"""
Module: filtered_logger
"""

import csv
import logging
import os
import mysql.connector
import re
from logging import Logger, StreamHandler
from logging.handlers import RotatingFileHandler


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting certain fields.

        Arguments:
        record: logging.LogRecord object representing the log record

        Returns:
        str: formatted log message with specified fields redacted
        """
        message = super().format(record)
        return filter_datum(
                self.fields, self.REDACTION, message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """
    Replace certain fields in a log message with a specified redaction.

    Arguments:
    fields: list of strings representing fields to obfuscate
    redaction: string representing the redaction to replace the fields with
    message: string representing the log line
    separator: string representing the character separating fields in the log
    line

    Returns:
    string: log message with specified fields obfuscated
    """
    return re.sub(fr'(?<= {separator} | ^)({" | ".join(fields)}=).*?({
            separator} | $)', fr'\1{redaction}\2', message)


def get_logger() -> Logger:
    """
    Get a configured logger object.

    Returns:
    logging.Logger: configured logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """
    Get a connector to the database.

    Returns:
    mysql.connector.connection.MySQLConnection: connector to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME", "")

    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=dbname
    )


def main():
    """
    Retrieve all rows in the users table and display each row under a
    filtered format.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        filtered_row = {
                key: "****" if key in PII_FIELDS else value for key,
                value in row.items()
                }
        logger.info(filtered_row)
    cursor.close()
    db.close()


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


if __name__ == "__main__":
    main()
