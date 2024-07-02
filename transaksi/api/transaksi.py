import structlog
import json
import sys

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from script.utils import (
    generateLog, LogLevel, 
    setSuccess, setError, setFailed,
)

from app.transaksi import TransaksiApp
from model.transaksi import Tabung, Tarik, Transfer, GetSaldo, GetMutasi

router = APIRouter()
log = structlog.get_logger('uvicorn')
transaksiApp = TransaksiApp()
auth_scheme = HTTPBearer()

@router.post("/tabung", description="Tabung saldo nasabah")
async def Tabung(request: Tabung, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    response = setSuccess("", "Berhasil menambah saldo tabungan!")
    try:
        response = transaksiApp.tabung(request)

        if response.get('status', 500) == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal menambah saldo tabungan!")
    # --

    return response
# --


@router.post("/tarik", description="Tarik saldo nasabah")
async def Tarik(request: Tarik, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    response = setSuccess("", "Berhasil menarik saldo!")
    try:
        response = transaksiApp.tarik(request)

        if response['status'] == 200:
            generateLog(LogLevel.INFO, "Success Response", "", response)
        else:
            generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)
    except Exception as e:
        response = setError("(99) Gagal menarik saldo!")
    # --

    return response
# --