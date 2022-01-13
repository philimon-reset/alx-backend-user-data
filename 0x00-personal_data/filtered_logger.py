#!/usr/bin/env python3
""" Write a function called filter_datum that returns log """
import logging
import re
from typing import List
from os import getenv
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:  # nopep8
    """ Filter logging """
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}', f'{i}={redaction}{separator}', message)  # nopep8
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the formatter """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format logrecord """
        return filter_datum(
            self.fields,
            self.REDACTION,
            super(RedactingFormatter, self).format(
                record),
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ get logger for csv file """
    logger = logging.getLogger("user_data")
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    cnx = mysql.connector.connect(
        user=getenv('PERSONAL_DATA_DB_USERNAME'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=getenv('PERSONAL_DATA_DB_HOST'),
        database=getenv('PERSONAL_DATA_DB_NAME'))
    return cnx


def main() -> None:
    """ generate mysql connector to the database """
    drop = get_db()
    cursor = drop.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    formatter = get_logger()
    for (
        name,
        email,
        ssn,
        phone,
        password,
        ip,
        last_login,
            user_agent) in cursor:
        message = f"name={name}; email={email}; phone={phone}; ssn={ssn}; password={password}; ip={ip}; last_login={last_login}; user_agent={user_agent};"  # nopep8
        formatter.info(message)

    cursor.close()
    drop.close()


if __name__ == '__main__':
    main()
