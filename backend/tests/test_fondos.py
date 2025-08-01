# backend/tests/test_fondos.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
id_fondo_existente = 1 # ID de fondo existente para pruebas

# -----------------------
# Tests de suscripción
# -----------------------

def test_suscripcion_exitosa():
    response = client.post("/fondos/suscribirse", json={
        "id_fondo": id_fondo_existente,
        "medio_notificacion": "email"
    })
    data = response.json()

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


# -----------------------
# Tests de cancelación
# -----------------------

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


# -----------------------
# Tests de historial
# -----------------------

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


# -----------------------
# Tests de saldo
# -----------------------


def test_saldo_inicial_sin_transacciones():
    user_id = "user-sin-transacciones"
    response = client.get("/fondos/saldo", headers={"x-user-id": user_id})
    assert response.status_code == 200
    assert response.json()["saldo"] == 500_000

def test_saldo_despues_de_apertura():
    user_id_test = "user-apertura"

    r = client.post("/fondos/suscribirse", json={
        "id_fondo": 5,
        "medio_notificacion": "email"
    }, headers={"x-user-id": user_id_test})

    assert r.status_code == 200
    transaccion_id = r.json()["transaccion"]["id"]

    # Verificar saldo
    r2 = client.get("/fondos/saldo", headers={"x-user-id": user_id_test})
    assert r2.status_code == 200
    assert r2.json()["saldo"] == 400_000

    # Limpieza
    client.delete(f"/fondos/transaccion/{transaccion_id}", headers={"x-user-id": user_id_test})

def test_saldo_despues_de_cancelacion():
    user_id_test = "user-cancelacion"

    # Limpieza previa
    historial = client.get("/fondos/historial", headers={"x-user-id": user_id_test})
    if historial.status_code == 200:
        for t in historial.json():
            client.delete(f"/fondos/transaccion/{t['id']}", headers={"x-user-id": user_id_test})

    # Suscribirse a fondo 3 ($50.000)
    r1 = client.post("/fondos/suscribirse", json={
        "id_fondo": 3,
        "medio_notificacion": "sms"
    }, headers={"x-user-id": user_id_test})
    assert r1.status_code == 200
    apertura_id = r1.json()["transaccion"]["id"]

    # Cancelar fondo 3
    r2 = client.post("/fondos/cancelar", json={
        "id_fondo": 3
    }, headers={"x-user-id": user_id_test})
    assert r2.status_code == 200
    cancelacion_id = r2.json()["transaccion"]["id"]

    # Verificar saldo
    r3 = client.get("/fondos/saldo", headers={"x-user-id": user_id_test})
    assert r3.status_code == 200
    assert r3.json()["saldo"] == 500_000

    # Limpieza final
    client.delete(f"/fondos/transaccion/{apertura_id}", headers={"x-user-id": user_id_test})
    client.delete(f"/fondos/transaccion/{cancelacion_id}", headers={"x-user-id": user_id_test})

def test_saldo_con_multiples_transacciones():
    user_id_test = "user-multiple"

    # Limpieza previa
    historial = client.get("/fondos/historial", headers={"x-user-id": user_id_test})
    if historial.status_code == 200:
        for t in historial.json():
            client.delete(f"/fondos/transaccion/{t['id']}", headers={"x-user-id": user_id_test})

    # Suscribirse a fondo 1 ($75.000)
    r1 = client.post("/fondos/suscribirse", json={
        "id_fondo": 1,
        "medio_notificacion": "sms"
    }, headers={"x-user-id": user_id_test})
    assert r1.status_code == 200
    apertura1_id = r1.json()["transaccion"]["id"]

    # Suscribirse a fondo 2 ($125.000)
    r2 = client.post("/fondos/suscribirse", json={
        "id_fondo": 2,
        "medio_notificacion": "sms"
    }, headers={"x-user-id": user_id_test})
    assert r2.status_code == 200
    apertura2_id = r2.json()["transaccion"]["id"]

    # Cancelar fondo 1 (+$75.000)
    r3 = client.post("/fondos/cancelar", json={
        "id_fondo": 1
    }, headers={"x-user-id": user_id_test})
    assert r3.status_code == 200
    cancelacion_id = r3.json()["transaccion"]["id"]

    # Saldo esperado: 500_000 - 75_000 - 125_000 + 75_000 = 375_000
    r4 = client.get("/fondos/saldo", headers={"x-user-id": user_id_test})
    assert r4.status_code == 200
    assert r4.json()["saldo"] == 375_000

    # Limpieza final
    client.delete(f"/fondos/transaccion/{apertura1_id}", headers={"x-user-id": user_id_test})
    client.delete(f"/fondos/transaccion/{apertura2_id}", headers={"x-user-id": user_id_test})
    client.delete(f"/fondos/transaccion/{cancelacion_id}", headers={"x-user-id": user_id_test})

