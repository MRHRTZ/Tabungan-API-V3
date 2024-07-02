from pydantic import BaseModel
from typing import Optional


class Nasabah(BaseModel):
    no_rekening: Optional[str]
    nama: Optional[str]
    nik: Optional[str]
    no_hp: Optional[str]
    pin: Optional[str]
    saldo:  Optional[int] = 0

class CreateNasabah(BaseModel):
    nama: Optional[str]
    nik: Optional[str]
    no_hp: Optional[str]
    pin: Optional[str]

class LoginNasabah(BaseModel):
    no_hp: Optional[str]
    pin: Optional[str]