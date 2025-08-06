from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import fondos

app = FastAPI(
    title="Gestor de Fondos de Inversión",
    description="API para suscripción, cancelación y consulta de transacciones de fondos.",
    version="1.0.0"
)

# Definir los orígenes permitidos (frontend), ajustar según sea necesario
origins = [
    "https://d3pi3yawthduvi.cloudfront.net",
]

# Aplicar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar rutas del router
app.include_router(fondos.router, prefix="/fondos", tags=["Fondos"])

@app.get("/")
def read_root(request: Request):
    base_url = str(request.base_url)
    return {
        "description": "La url de la documentación es la siguiente",
        "url": f"{base_url}docs"
    }

