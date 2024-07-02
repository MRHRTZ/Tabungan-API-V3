import os
import redis
import structlog

from fastapi import FastAPI, BackgroundTasks
from api import api_router
from dotenv import load_dotenv
from app.transaksi import TransaksiApp
load_dotenv()

app = FastAPI(title="Mutasi API", version="3.0.0")
log = structlog.get_logger('uvicorn')

app.include_router(api_router)
    