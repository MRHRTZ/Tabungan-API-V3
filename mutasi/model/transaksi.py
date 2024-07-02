from pydantic import BaseModel
from typing import Optional

class Tabung(BaseModel):
    no_rekening: Optional[str]
    nominal: Optional[int]

class Tarik(BaseModel):
    no_rekening: Optional[str]
    nominal: Optional[int]

class Transfer(BaseModel):
    no_rekening_asal: Optional[str]
    no_rekening_tujuan: Optional[str]
    nominal: Optional[int]

class GetSaldo(BaseModel):
    no_rekening: Optional[str]

class GetMutasi(BaseModel):
    tanggal_transaksi: Optional[str]
    no_rekening: Optional[str]
    jenis_transaksi: Optional[str]
    nominal:  Optional[int] = 0

class CreateTransaction(BaseModel):
    no_rekening: Optional[str]
    jenis_transaksi: Optional[str]
    nominal: Optional[int]
    waktu: Optional[str]

class ResponseMutation(BaseModel):
    waktu: Optional[str]
    jenis_transaksi: Optional[str]
    nominal: Optional[int]

class Transaction(BaseModel):
    id_transaksi: Optional[int]
    no_rekening: Optional[str]
    jenis_transaksi: Optional[str]
    nominal: Optional[int]
    waktu: Optional[str]