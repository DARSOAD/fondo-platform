# backend/tests/test_fondos.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
id_fondo_existente = 1 # ID de fondo existente para pruebas

def test_suscripcion_exitosa():
    response = client.post("/fondos/suscribirse", json={
        "id_fondo": id_fondo_existente,
        "medio_notificacion": "email"
    })
    data = response.json()
    
    print("POST /fondos/suscribirse status:", response.status_code)
    print("Respuesta de suscripción:", data)

    assert response.status_code == 200
    assert "transaccion" in data
    assert data["transaccion"]["tipo"] == "apertura"
    assert data["transaccion"]["fondo_id"] == id_fondo_existente

    # Limpieza
    transaccion_id = data["transaccion"]["id"]
    print("Intentando eliminar transacción con ID:", transaccion_id)

    delete_resp = client.delete(f"/fondos/transaccion/{transaccion_id}")
    print("DELETE status:", delete_resp.status_code)
    print("Respuesta de eliminación:", delete_resp.json())

    assert delete_resp.status_code == 200
    assert "eliminada" in delete_resp.json()["mensaje"]



def test_fondo_no_existe():
    response = client.post("/fondos/suscribirse", json={
        "id_fondo": 999,
        "medio_notificacion": "sms"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Fondo no encontrado"


def test_suscripcion_duplicada():
    # Primer intento
    r1 = client.post("/fondos/suscribirse", json={"id_fondo": id_fondo_existente})
    assert r1.status_code == 200
    transaccion_id = r1.json()["transaccion"]["id"]

    # Segundo intento (debería fallar)
    r2 = client.post("/fondos/suscribirse", json={"id_fondo": id_fondo_existente})
    assert r2.status_code == 400
    assert "Ya estás inscrito" in r2.json()["detail"]

    # Limpieza
    delete_resp = client.delete(f"/fondos/transaccion/{transaccion_id}")
    assert delete_resp.status_code == 200

def test_body_invalido():
    response = client.post("/fondos/suscribirse", json={})
    assert response.status_code == 422



def test_cancelar_exitosamente():
    # Suscripción
    r1 = client.post("/fondos/suscribirse", json={"id_fondo": id_fondo_existente})
    assert r1.status_code == 200
    trans_id = r1.json()["transaccion"]["id"]

    # Cancelación
    r2 = client.post("/fondos/cancelar", json={"id_fondo": id_fondo_existente})
    data = r2.json()
    assert r2.status_code == 200
    assert data["transaccion"]["tipo"] == "cancelacion"
    assert data["transaccion"]["fondo_id"] == id_fondo_existente

    # Limpieza
    client.delete(f"/fondos/transaccion/{trans_id}")
    client.delete(f"/fondos/transaccion/{data['transaccion']['id']}")

def test_cancelar_sin_estar_inscrito():
    response = client.post("/fondos/cancelar", json={"id_fondo": id_fondo_existente})
    assert response.status_code == 400
    assert "No estás inscrito" in response.json()["detail"]

def test_cancelar_fondo_inexistente():
    response = client.post("/fondos/cancelar", json={"id_fondo": 999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Fondo no encontrado"

def test_cancelar_dos_veces():
    # Suscribirse y cancelar una vez
    r1 = client.post("/fondos/suscribirse", json={"id_fondo": id_fondo_existente})
    assert r1.status_code == 200
    apertura_id = r1.json()["transaccion"]["id"]

    r2 = client.post("/fondos/cancelar", json={"id_fondo": id_fondo_existente})
    assert r2.status_code == 200
    cancelacion_id = r2.json()["transaccion"]["id"]

    # Segundo intento de cancelación
    r3 = client.post("/fondos/cancelar", json={"id_fondo": id_fondo_existente})
    assert r3.status_code == 400
    assert "No estás inscrito" in r3.json()["detail"]

    # Limpieza
    client.delete(f"/fondos/transaccion/{apertura_id}")
    client.delete(f"/fondos/transaccion/{cancelacion_id}")

def test_historial_exitoso():
    # En caso de que no haya transacciones, se crea una
    r1 = client.post("/fondos/suscribirse", json={"id_fondo": id_fondo_existente})
    assert r1.status_code == 200
    trans_id = r1.json()["transaccion"]["id"]

    # Obtener historial
    r2 = client.get("/fondos/historial")
    data = r2.json()
    assert r2.status_code == 200
    assert isinstance(data, list)
    assert any(t["id"] == trans_id for t in data)

    # Limpieza
    client.delete(f"/fondos/transaccion/{trans_id}")

def test_historial_vacio():
    test_user = "test-user-historial-vacio"

    # Verifica si hay transacciones para ese usuario (debería estar vacío si es nuevo)
    r = client.get("/fondos/historial", headers={"x-user-id": test_user})
    if r.status_code == 200:
        # Si por alguna razón hay transacciones, eliminarlas
        for t in r.json():
            client.delete(f"/fondos/transaccion/{t['id']}")

    # Segunda llamada, debería estar vacío
    r2 = client.get("/fondos/historial", headers={"x-user-id": test_user})
    assert r2.status_code == 404
    assert r2.json()["detail"] == "No hay transacciones registradas"



