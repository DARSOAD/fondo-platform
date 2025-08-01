# backend/schemas/transaccion.py
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class OperacionFondo(BaseModel):
    id_fondo: int
    medio_notificacion: Optional[str] = "email"

class TransaccionOut(BaseModel):
    id: str
    usuario_id: str
    tipo: Literal["apertura", "cancelacion"]
    fondo_id: int
    fondo_nombre: str
    valor: int
    medio: Literal["email", "sms"]
    timestamp: datetime
    categoria: Literal["FPV", "FIC"]

class SuscripcionResponse(BaseModel):
    mensaje: str
    transaccion: TransaccionOut
    saldo_restante: int
