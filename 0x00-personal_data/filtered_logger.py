#!/usr/bin/env python3
""" Write a function called filter_datum that returns log """
import logging
import re
from typing import List
PII_FIELDS = ("name", "email", "ssn", "password", "ip")


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> List:
    """ Filter logging """
    regex = message.split(separator)
    new = []
    for i in regex:
        if i.split("=")[0] in fields:
            new.append(re.sub(i.split("=")[1], redaction, i))
        else:
            new.append(i)
    separator += ' '
    return separator.join(new)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        """ Initialize the formatter """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format logrecord """
        return filter_datum(
            self.fields,
            self.REDACTION,
            logging.Formatter.format(
                self,
                record),
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ get logger for csv file """
    logger = logging.getLogger("user_data")
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter)
    logging.LoggerAdapter(logging.getLogger('user_data'), PII_FIELDS)
    logger.addHandler(stream)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    return logger
