from fastapi import FastAPI
from routers import fondos

app = FastAPI(
    title="Gestor de Fondos de Inversión",
    description="API para suscripción, cancelación y consulta de transacciones de fondos.",
    version="1.0.0"
)

# Cargar el router de fondos
app.include_router(fondos.router, prefix="/fondos", tags=["Fondos"])

# Endpoint de prueba
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"} 