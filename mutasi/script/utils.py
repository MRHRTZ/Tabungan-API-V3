import structlog
import time
import random
import os
import traceback
import pytz
import enum
import bcrypt

from pydantic import BaseModel
from typing import Tuple
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, Literal

log = structlog.get_logger('uvicorn')

class RandomType(enum.Enum):
    STRING: str = 'S'
    INTEGER: str = 'I'

class LogLevel(enum.Enum):
    DEBUG: str = 'D'
    INFO: str = 'I'
    WARNING: str = 'W'
    ERROR: str = 'E'
    CRITICAL: str = 'C'

def encrypt_string(string, round=10):
    return bcrypt.hashpw(string.encode(), bcrypt.gensalt())

def verify_encrypt(string, encrypted):
    return bcrypt.checkpw(string, encrypted).decode()

def get_random(random_type: Literal[RandomType.STRING, RandomType.INTEGER] = RandomType.INTEGER, length: int = 3) -> str:
    if random_type == RandomType.STRING:
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits)
                             for i in range(length)))
    else:
        range_start = 10**(length-1)
        range_end = (10**length)-1
        result_str = str(random.randint(range_start, range_end))

    return result_str


def response_message(status: int = 200, remark: str = "", data: str = "", trace_before: int = "") -> dict:
    resp = {
        'trace': get_random(RandomType.INTEGER.value, 15),
        'status': status,
        'remark': remark,
        'result': data
    }

    return resp

def generateLog(
    logLevel:  Literal[LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL], 
    title: str,
    msg: str = "",
    data: any = "",
):
    title = title if title else '-'
    strGen = "\n"
    strGen += "="*10 + f"[ {title} ]" + "="*10+"\n"
    strGen += "Message : " + (str(msg) if msg else '-')+"\n"
    strGen += "Response : " + (str(data) if data else '-')+"\n"
    strGen += "="*(24+len(title))
    
    if logLevel == LogLevel.DEBUG:
        log.debug(strGen)
    elif logLevel == LogLevel.INFO:
        log.info(strGen)
    elif logLevel == LogLevel.WARNING:
        log.warn(strGen)
    elif logLevel == LogLevel.ERROR:
        log.error(strGen)
    elif logLevel == LogLevel.CRITICAL:
        log.critical(strGen)

def setSuccess(data: str, remark: str = "") -> None:
    resp = response_message(200, remark, data)

    return resp


def setFailed(remark: str) -> None:
    resp = response_message(400, remark, "")

    return resp


def setError(remark: str) -> None:
    resp = response_message(500, remark, "")
    generateLog(LogLevel.ERROR, "Error Response", traceback.format_exc(), resp)

    return resp

def getCurrentTime(format: str = '%Y-%m-%d %H:%M:%S') -> str:
    current_datetime = datetime.now()
    tz = os.environ.get('TIMEZONE')
    generateLog(LogLevel.DEBUG, "test date", tz)
    timezone = pytz.timezone(tz)
    current_datetime_wib = current_datetime.astimezone(timezone)
    formatted_time = current_datetime_wib.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time

def generate_insert_sql_from_model(table_name: str, model: BaseModel) -> Tuple[str, tuple]:
    columns = model.__annotations__.keys()
    values = [getattr(model, column) for column in columns]

    column_names = ', '.join(columns)
    placeholders = ', '.join(["'%s'"] * len(values))

    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    return insert_sql, tuple(values)

def generate_update_sql_from_model(table_name: str, model: BaseModel, condition: str) -> Tuple[str, tuple]:
    columns = model.__annotations__.keys()
    values = [getattr(model, column) for column in columns]

    set_clauses = ', '.join([f"{column} = %s" for column in columns])

    update_sql = f"UPDATE {table_name} SET {set_clauses} WHERE {condition}"
    return update_sql, tuple(values)

def generate_insert_sql(table_name: str, data: str) -> Tuple[str, tuple]:
    columns = list(data.keys())
    values = list(data.values())

    column_names = ', '.join(columns)
    placeholders = ', '.join(["'%s'"] * len(values))

    insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    return insert_sql, tuple(values)

def generate_update_sql(table_name: str, data: str, condition: str) -> Tuple[str, tuple]:
    columns = list(data.keys())
    values = list(data.values())

    set_clauses = ', '.join([f"{column} = %s" for column in columns])

    update_sql = f"UPDATE {table_name} SET {set_clauses} WHERE {condition}"
    return update_sql, tuple(values)