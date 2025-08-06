# backend/schemas/transaccion.py
from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from datetime import datetime
import re

class OperacionFondo(BaseModel):
    id_fondo: int
    medio_notificacion: Optional[str] = "email"
    usuario_contacto: str  
    @field_validator("usuario_contacto")
    def validar_usuario_contacto(cls, v, info):
        medio = info.data.get("medio_notificacion")

        if medio == "email":
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
                raise ValueError("El email proporcionado no es válido")
        elif medio == "sms":
            if not re.match(r"^\+\d{10,15}$", v):
                raise ValueError("El número debe estar en formato internacional (ej: +573001234567)")
        return v

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
    usuario_contacto: str

class SuscripcionResponse(BaseModel):
    mensaje: str
    transaccion: TransaccionOut
    saldo_restante: int

