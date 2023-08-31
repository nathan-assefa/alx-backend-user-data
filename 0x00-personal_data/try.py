#!/usr/bin/env python3
''' Filtering log '''
import re
from typing import List

'''
def filter_datum(field, redaction, message, separator):
'''

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Return an obfuscated log message
    Args:
        fields (list): list of strings indicating fields to obfuscate
        redaction (str): what the field will be obfuscated to
        message (str): the log line to obfuscate
        separator (str): the character separating the fields
    """
    for field in fields:
        rg = re.search(r'(=.*?)', message)

        if rg:
            print("Found:", rg.group())
        else:
            print("Pattern not found")
        print(f'{field}{rg.group()}{separator}')

        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message
