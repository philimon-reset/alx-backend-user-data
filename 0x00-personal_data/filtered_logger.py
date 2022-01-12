#!/usr/bin/env python3
""" Write a function called filter_datum that returns log """
import logging
import re
from typing import List
PII_FIELDS = ("name", "email", "ssn", "password", "ip")


def filter_datum(
        fields: List,
        redaction: str,
        message: str,
        separator: str) -> str:
    """ Filter logging """
    for i in fields:
        message = re.sub(fr'{i}=.+?{separator}', f'{i}={redaction}{separator}', message)
    return message