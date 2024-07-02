import structlog
import sys

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from script.utils import generateLog, LogLevel, setSuccess, setError, setFailed

from app.nasabah import NasabahApp
from model.nasabah import CreateNasabah, LoginNasabah

router = APIRouter()
log = structlog.get_logger('uvicorn')
nasabahApp = NasabahApp()

@router.post("/daftar", description="Pendaftaran Nasabah")
async def Register_User(request: CreateNasabah):    
    response = nasabahApp.daftar_nasabah(request)

    if response.get('status', 500) == 200:
        generateLog(LogLevel.INFO, "Success Response", "", response)
    else:
        generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    # --

    return response
# --

@router.post("/login", description="Login Nasabah")
async def Login(request: LoginNasabah):    
    response = nasabahApp.login(request)

    if response.get('status', 500) == 200:
        generateLog(LogLevel.INFO, "Success Response", "", response)
    else:
        generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    # --

    return response
# --
