from fastapi import FastAPI
from app.routes import router
from app.services.cleaner import limpiar_directorios_temporales

app = FastAPI(
    title="API CNN-LSTM para Procesamiento de Imágenes .tif",
    description="Esta API permite descargar, normalizar, parchear y almacenar imágenes .tif en una base de datos PostgreSQL.",
    version="1.0.0"
)

# Limpieza inicial al arrancar
@app.on_event("startup")
def iniciar_limpieza():
    limpiar_directorios_temporales()

# Incluir rutas
app.include_router(router)
