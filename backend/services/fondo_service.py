# backend/services/fondo_service.py

from fastapi import HTTPException
from services.notificacion_service import enviar_notificacion
from db.dynamodb import dynamodb
from models.transaccion_model import Transaccion

tabla = dynamodb.Table("transacciones")

def guardar_transaccion(usuario_id, tipo, fondo_id, fondo_nombre, valor, medio, categoria, usuario_contacto):
    try:
        transaccion = Transaccion(
            usuario_id=usuario_id,
            tipo=tipo,
            fondo_id=fondo_id,
            fondo_nombre=fondo_nombre,
            valor=valor,
            medio=medio,
            categoria=categoria,
            usuario_contacto=usuario_contacto  
        )

        tabla.put_item(Item=transaccion.to_dict())

        enviar_notificacion(medio, f"Te suscribiste al fondo {fondo_nombre}", usuario_contacto)

        return transaccion.to_dict()

    except TypeError as te:
        raise HTTPException(
            status_code=422,
            detail=f"Error en la creación de la transacción: {str(te)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al guardar la transacción: {str(e)}"
        )


def esta_inscrito(usuario_id, fondo_id):
    response = tabla.scan(
        FilterExpression="usuario_id = :uid AND fondo_id = :fid",
        ExpressionAttributeValues={
            ":uid": usuario_id,
            ":fid": fondo_id
        }
    )

    transacciones = response.get("Items", [])

    if not transacciones:
        return False
    
    ordenadas = sorted(transacciones, key=lambda t: t["timestamp"], reverse=True)

    ultima = ordenadas[0]
    return ultima["tipo"] == "apertura"


def cancelar_transaccion(usuario_id, fondo_id, usuario_contacto, medio):
    response = tabla.scan(
        FilterExpression="usuario_id = :uid AND fondo_id = :fid",
        ExpressionAttributeValues={
            ":uid": usuario_id,
            ":fid": fondo_id
        }
    )

    transacciones = response.get("Items", [])
    ordenadas = sorted(transacciones, key=lambda x: x['timestamp'], reverse=True)

    ultima_apertura = next((t for t in ordenadas if t["tipo"] == "apertura"), None)
    ultima_cancelacion = next((t for t in ordenadas if t["tipo"] == "cancelacion"), None)

    if not ultima_apertura or (ultima_cancelacion and ultima_cancelacion["timestamp"] > ultima_apertura["timestamp"]):
        return None

    transaccion = Transaccion(
        usuario_id=usuario_id,
        tipo="cancelacion",
        fondo_id=fondo_id,
        fondo_nombre=ultima_apertura["fondo_nombre"],
        valor=ultima_apertura["valor"],
        medio=medio,  
        categoria=ultima_apertura["categoria"],
        usuario_contacto=usuario_contacto
    )

    try:
        tabla.put_item(Item=transaccion.to_dict())
        enviar_notificacion(transaccion.medio, f"Cancelaste tu suscripción al fondo {transaccion.fondo_nombre}", usuario_contacto)
    except Exception as e:
        raise Exception(f"Error al guardar transacción de cancelación en DynamoDB: {str(e)}")

    return transaccion.to_dict()

def obtener_historial(usuario_id):
    """
    Consulta las transacciones del usuario desde DynamoDB.

    Actualmente limitado a un máximo de 10 registros recientes.

    ✳️ NOTA: Para escalar a paginación real, esta función puede extenderse
    con soporte a parámetros 'limit' y 'start_key', usando:
    - Limit=<int>
    - ExclusiveStartKey={'id': <last_id>, 'usuario_id': <user_id>}
    """

    response = tabla.scan(
        FilterExpression="usuario_id = :uid",
        ExpressionAttributeValues={":uid": usuario_id}
    )

    items = response.get("Items", [])

    # Ordenar manualmente por timestamp descendente (más recientes primero)
    items.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    # Limitar a las 10 transacciones más recientes
    return items[:10]


def calcular_saldo_usuario(usuario_id: str) -> int:
    transacciones = obtener_historial(usuario_id)
    saldo_inicial = 500000
    for t in transacciones:
        if t["tipo"] == "apertura":
            saldo_inicial -= t["valor"]
        elif t["tipo"] == "cancelacion":
            saldo_inicial += t["valor"]
    return saldo_inicial
