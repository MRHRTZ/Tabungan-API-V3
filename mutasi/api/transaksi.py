import structlog
import sys

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from script.utils import (
    generateLog, LogLevel, 
    setSuccess, setError, setFailed,
)

from app.transaksi import TransaksiApp
from model.transaksi import Tabung, Tarik, Transfer, GetSaldo, GetMutasi

router = APIRouter()
log = structlog.get_logger('uvicorn')
transaksiApp = TransaksiApp()

@router.post("/mutasi", description="Mutasi nasabah")
async def mutasi(request: GetMutasi):
    response = transaksiApp.mutasi(request)

    if response.get('status', 500) == 200:
        generateLog(LogLevel.INFO, "Success Response", "", response)
    else:
        generateLog(LogLevel.WARNING, "Failed Response", response['remark'], response)

    return response
# --
