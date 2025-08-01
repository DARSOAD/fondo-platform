# backend/services/fondo_service.py
from services.notificacion_service import enviar_notificacion
from db.dynamodb import dynamodb
from models.transaccion_model import Transaccion

tabla = dynamodb.Table("Transacciones")

def guardar_transaccion(usuario_id, tipo, fondo_id, fondo_nombre, valor, medio, categoria):
    transaccion = Transaccion(
        usuario_id=usuario_id,
        tipo=tipo,
        fondo_id=fondo_id,
        fondo_nombre=fondo_nombre,
        valor=valor,
        medio=medio,
        categoria=categoria
    )

    try:
        tabla.put_item(Item=transaccion.to_dict())
        enviar_notificacion(usuario_id, medio, f"Te suscribiste al fondo {fondo_nombre}")

    except Exception as e:
        raise Exception(f"Error al guardar transacción en DynamoDB: {str(e)}")

    return transaccion.to_dict()

def esta_inscrito(usuario_id, fondo_id):
    tabla = dynamodb.Table("Transacciones")
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


def cancelar_transaccion(usuario_id, fondo_id):
    tabla = dynamodb.Table("Transacciones")

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

    print(f"Última apertura: {ultima_apertura}, Última cancelación: {ultima_cancelacion}")

    if not ultima_apertura or (ultima_cancelacion and ultima_cancelacion["timestamp"] > ultima_apertura["timestamp"]):
        return None

    transaccion = Transaccion(
        usuario_id=usuario_id,
        tipo="cancelacion",
        fondo_id=fondo_id,
        fondo_nombre=ultima_apertura["fondo_nombre"],
        valor=ultima_apertura["valor"],
        medio="email",  
        categoria=ultima_apertura["categoria"]
    )

    try:
        tabla.put_item(Item=transaccion.to_dict())
        enviar_notificacion(usuario_id, transaccion.medio, f"Cancelaste tu suscripción al fondo {transaccion.fondo_nombre}")
    except Exception as e:
        raise Exception(f"Error al guardar transacción de cancelación en DynamoDB: {str(e)}")

    return transaccion.to_dict()

def obtener_historial(usuario_id):
    tabla = dynamodb.Table("Transacciones")
    response = tabla.scan(
        FilterExpression="usuario_id = :uid",
        ExpressionAttributeValues={":uid": usuario_id}
    )
    return response.get("Items", [])
