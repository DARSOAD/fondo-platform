# backend/models/transaccion_model.py
from datetime import datetime
import uuid

class Transaccion:
    def __init__(self, usuario_id, tipo, fondo_id, fondo_nombre, valor, medio, categoria, usuario_contacto):
        self.id = str(uuid.uuid4())
        self.usuario_id = usuario_id
        self.tipo = tipo  # "apertura" o "cancelación"
        self.fondo_id = fondo_id
        self.fondo_nombre = fondo_nombre
        self.valor = valor
        self.medio = medio  # "email" o "sms"
        self.timestamp = datetime.utcnow().isoformat()
        self.categoria = categoria
        self.usuario_contacto = usuario_contacto

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "fondo_id": self.fondo_id,
            "fondo_nombre": self.fondo_nombre,
            "valor": self.valor,
            "medio": self.medio,
            "timestamp": self.timestamp,
            "categoria": self.categoria,
            "usuario_contacto": self.usuario_contacto
        }
