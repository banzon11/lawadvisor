from datetime import datetime
import re

def to_datetime(date):
    obj_datetime = datetime.strptime(date, '%d/%m/%Y')
    return obj_datetime


def isValidDateFormat(date):
    if isinstance(date, float):
        return True

    try:
        date = to_datetime(date)
        if date < datetime.today():
            return False
        return True
    except:
        return False


def isEmailValid(email):

    if isinstance(email, float):
        return True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


def validate_string_type(data):
    try:
        str(data)
        return True
    except:
        return False


def validate_integer_type(data):
    try:
        int(data)
        return True
    except:
        if validate_float_type(data):
            return True

        return False


def validate_float_type(data):
    try:
        float(data)
        return True
    except:
        return False


def string_to_list(string):
    if string == "":
        return []
    listObj = string.split(",")
    return [int(e) for e in listObj]


def list_to_string(listObj):

    stringList = [str(e) for e in listObj]
    return ",".join(stringList)
