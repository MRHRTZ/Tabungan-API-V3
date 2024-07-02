import structlog
import time
import random
import os
import traceback
import pytz
import enum
import bcrypt
import jwt
import redis
import requests

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Tuple
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, Literal
load_dotenv()

log = structlog.get_logger('uvicorn')

secret = "MYTABUNGAN@2024"

mutasi_baseurl = os.getenv('MTT_HOST')
mutasi_port = os.getenv('MTT_PORT').split(':')[-1]

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_EXPOSE', '6379')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

class RandomType(enum.Enum):
    STRING: str = 'S'
    INTEGER: str = 'I'

class LogLevel(enum.Enum):
    DEBUG: str = 'D'
    INFO: str = 'I'
    WARNING: str = 'W'
    ERROR: str = 'E'
    CRITICAL: str = 'C'

def redis_dependency(request: Request):
    request.state.redis = redis_client
   
def encode_jwt(payload):
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(encoded):
    return jwt.decode(encoded, secret, algorithms=["HS256"])

def encrypt_string(string, round=10):
    return bcrypt.hashpw(string.encode(), bcrypt.gensalt())

def verify_encrypt(plain, encrypted):
    return bcrypt.checkpw(plain.encode(), encrypted.encode())

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


def setFailed(remark: str, status_code: int = 400) -> None:
    resp = response_message(status_code, remark, "")

    return resp


def setError(remark: str, status_code: int = 500) -> None:
    resp = response_message(status_code, remark, "")
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

def get_token_from_request(request):
    if "Authorization" not in request.headers:
        return False
    token_header = request.headers["Authorization"]
    if token_header.startswith("Bearer "):
        return token_header.split("Bearer ")[-1]
    else:
        return False

def verify_access_token(request):
    token = get_token_from_request(request)
    
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Bearer token tidak ada")
        #--
        payload = decode_jwt(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token kadaluarsa")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token tidak valid")
    

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/api/v1/transaksi"):
            try:
                # Call the verify_access_token function to validate the token
                verify_access_token(request)
                # If token validation succeeds, continue to the next middleware or route handler
                response = await call_next(request)
                return response
            except HTTPException as exc:
                # If token validation fails due to HTTPException, return the error response
                resp = setError(exc.detail, exc.status_code)
                return JSONResponse(content=resp, status_code=exc.status_code)
            except Exception as exc:
                # If token validation fails due to other exceptions, return a generic error response
                resp = setError(str(exc), 500)
                return JSONResponse(content=resp, status_code=500)
        else:
            response = await call_next(request)
            return response
        # --
    # --
# --

def svc_mutasi(endpoint, payload, method='POST'):
    try:
        response = setFailed('Gagal HIT Service Mutasi')
        url = f'http://{mutasi_baseurl}:{mutasi_port}{endpoint}'
        print('URL:', url)
        if method == 'POST':
            response = requests.post(url, data=payload).json()
        else:
            response = requests.get(url).json()
        return response
    except Exception as e:
        return setError(str(e))