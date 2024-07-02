import structlog

from fastapi import FastAPI, Request
from api import api_router
from script.utils import CustomMiddleware

app = FastAPI(title="API Transaksi", version="3.0.0")
log = structlog.get_logger('uvicorn')
 
app.add_middleware(CustomMiddleware)
app.include_router(api_router)