# backend/services/notificacion_service.py

def enviar_notificacion(usuario_id: str, medio: str, mensaje: str):
    if medio == "email":
        print(f"[SIMULACIÓN] Enviando correo a {usuario_id}: {mensaje}") # Simulación de envío de correo
    elif medio == "sms":
        print(f"[SIMULACIÓN] Enviando SMS a {usuario_id}: {mensaje}") # Simulación de envío de SMS
    else:
        print(f"[ERROR] Medio de notificación no válido: {medio}") # Simulación de error
        raise ValueError("Medio de notificación no válido")
