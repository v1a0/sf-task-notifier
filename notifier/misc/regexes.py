import re

PHONE_NUMBER = r'^1?\d{9,15}$'
PHONE_NUMBER_PLUS = r'^\+?1?\d{9,15}$'


def is_phone_number_valid(value: str) -> bool:
    return bool(re.fullmatch(PHONE_NUMBER, value))
