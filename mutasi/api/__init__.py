from fastapi import APIRouter
from . import transaksi

api_router = APIRouter()

prefix = '/api/v1'

api_router.include_router(transaksi.router, prefix=prefix, tags=["Transaksi"])