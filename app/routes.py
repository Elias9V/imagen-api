# routes.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.drive_service import descargar_ultimo_tif_drive
from app.services.normalizer import normalizar_tif
from app.services.patcher import generar_patches
from app.services.cleaner import eliminar_archivo_si_existe, eliminar_directorio_si_existe
from app.db.crud import guardar_en_bd, listar_imagenes, eliminar_imagen_y_patches, buscar_imagen_por_id

router = APIRouter()

@router.post("/procesar")
def procesar_pipeline():
    try:
        # Paso 1: Descargar
        ruta_descarga = descargar_ultimo_tif_drive()

        # Paso 2: Normalizar
        ruta_normalizada = normalizar_tif(ruta_descarga)

        # Paso 3: Parches
        carpeta_patches = generar_patches(ruta_normalizada)

        # Paso 4: Guardar en BD
        guardar_en_bd(ruta_normalizada, carpeta_patches)

        # Paso 5: Limpieza local
        eliminar_archivo_si_existe(ruta_descarga)
        eliminar_archivo_si_existe(ruta_normalizada)
        eliminar_directorio_si_existe(carpeta_patches)

        return JSONResponse({
            "mensaje": "✅ Imagen procesada, parcheada y registrada correctamente en la base de datos."
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/listar")
def listar():
    try:
        datos = listar_imagenes()
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/buscar_por_id/{imagen_id}")
def buscar_por_id(imagen_id: int):
    resultado = buscar_imagen_por_id(imagen_id)
    if resultado:
        return resultado
    return JSONResponse(status_code=404, content={"error": "Imagen no encontrada"})


@router.delete("/eliminar/{imagen_id}")
def eliminar(imagen_id: int):
    try:
        eliminar_imagen_y_patches(imagen_id)
        return {"mensaje": f"✅ Imagen con ID {imagen_id} y sus parches fueron eliminados."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
