# routes.py

import io
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from app.services.drive_service import descargar_ultimo_tif_drive
from app.services.normalizer import normalizar_tif
from app.services.patcher import generar_patches
from app.services.cleaner import eliminar_archivo_si_existe, eliminar_directorio_si_existe
from app.db.crud import guardar_en_bd, listar_imagenes, eliminar_imagen_y_patches, buscar_imagen_por_id, obtener_archivo_binario, obtener_parche_binario
from app.services.generator import generar_y_exportar_imagen
from app.db.request_models import ImagenRequest

router = APIRouter()

@router.get("/descargar_parche/{id}")
def descargar_parche(id: int):
    resultado = obtener_parche_binario(id)

    if not resultado:
        raise HTTPException(status_code=404, detail="❌ Parche no encontrado.")

    nombre_parche, archivo_bytes = resultado

    return StreamingResponse(
        io.BytesIO(archivo_bytes),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={nombre_parche}"}
    )

@router.get("/descargar_normalizado/{id}")
def descargar_normalizado(id: int):
    resultado = obtener_archivo_binario(id)
    if not resultado:
        return {"status": "error", "mensaje": "❌ Archivo no encontrado."}
    
    nombre, binario = resultado
    return StreamingResponse(io.BytesIO(binario), 
                             media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={nombre}"})

@router.post("/generar_imagen")
def generar_imagen(req: ImagenRequest):
    return generar_y_exportar_imagen(
        fecha_inicio=req.fecha_inicio,
        fecha_fin=req.fecha_fin,
        coordenadas=req.coordenadas
    )

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
