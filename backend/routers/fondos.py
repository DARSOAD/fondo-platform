# backend/routers/fondos.py
from fastapi import APIRouter, HTTPException, Header
from schemas.transaccion import OperacionFondo, SuscripcionResponse, TransaccionOut
from typing import List
from services.fondo_service import guardar_transaccion, esta_inscrito, cancelar_transaccion, obtener_historial


router = APIRouter()

# Datos simulados de fondos
fondos_disponibles = {
    1: {"nombre": "FPV_EL CLIENTE_RECAUDADORA", "monto_min": 75000, "categoria": "FPV"},
    2: {"nombre": "FPV_EL CLIENTE_ECOPETROL", "monto_min": 125000, "categoria": "FPV"},
    3: {"nombre": "DEUDAPRIVADA", "monto_min": 50000, "categoria": "FIC"},
    4: {"nombre": "FDO-ACCIONES", "monto_min": 250000, "categoria": "FIC"},
    5: {"nombre": "FPV_EL CLIENTE_DINAMICA", "monto_min": 100000, "categoria": "FPV"},
}

saldo_usuario = 500000  # variable temporal


@router.post("/suscribirse", response_model=SuscripcionResponse)
def suscribirse(
        data: OperacionFondo,
        x_user_id: str = Header(default="user-001")
    ):
    global saldo_usuario

    fondo = fondos_disponibles.get(data.id_fondo)
    if not fondo:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    if esta_inscrito("user-001", data.id_fondo):
        raise HTTPException(status_code=400, detail=f"Ya estás inscrito en el fondo {fondo['nombre']}")

    if saldo_usuario < fondo["monto_min"]:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}"
        )

    saldo_usuario -= fondo["monto_min"]

    transaccion = guardar_transaccion(
        usuario_id=x_user_id, # ID de usuario simulado
        tipo="apertura",
        fondo_id=data.id_fondo,
        fondo_nombre=fondo["nombre"],
        valor=fondo["monto_min"],
        medio=data.medio_notificacion,
        categoria=fondo["categoria"]
    )

    return {
        "mensaje": "Suscripción exitosa",
        "transaccion": transaccion,
        "saldo_restante": saldo_usuario
    }

@router.delete("/transaccion/{transaccion_id}")
def eliminar_transaccion(transaccion_id: str):
    from db.dynamodb import dynamodb
    tabla = dynamodb.Table("Transacciones")

    try:
        tabla.delete_item(Key={"id": transaccion_id})
        return {"mensaje": f"Transacción {transaccion_id} eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")
    
@router.post("/cancelar", response_model=SuscripcionResponse)
def cancelar(
        data: OperacionFondo,
        x_user_id: str = Header(default="user-001") # ID de usuario simulado
    ):
    fondo = fondos_disponibles.get(data.id_fondo)
    if not fondo:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    resultado = cancelar_transaccion(
        usuario_id=x_user_id,
        fondo_id=data.id_fondo
    )

    if not resultado:
        raise HTTPException(status_code=400, detail="No estás inscrito en este fondo o ya lo cancelaste")

    return {
        "mensaje": f"Cancelación exitosa del fondo {fondo['nombre']}",
        "transaccion": resultado,
        "saldo_restante": saldo_usuario + resultado["valor"]  
    }

@router.get("/historial", response_model=List[TransaccionOut])
def historial(x_user_id: str = Header(default="user-001")): # ID de usuario simulado
    transacciones = obtener_historial(x_user_id)
    if not transacciones:
        raise HTTPException(status_code=404, detail="No hay transacciones registradas")
    return transacciones

