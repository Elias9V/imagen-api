# services/cleaner.py
import os
import shutil

def limpiar_directorios_temporales():
    carpetas = ["data/raw", "data/normalized", "data/patches/patches"]
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
        os.makedirs(carpeta, exist_ok=True)
    print("🧹 Directorios temporales limpiados.")

def eliminar_archivo_si_existe(ruta):
    if os.path.isfile(ruta):
        os.remove(ruta)
        print(f"🗑 Archivo eliminado: {ruta}")

def eliminar_contenido_directorio(ruta):
    if os.path.isdir(ruta):
        for archivo in os.listdir(ruta):
            ruta_archivo = os.path.join(ruta, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        print(f"📁 Contenido del directorio '{ruta}' eliminado.")

def eliminar_directorio_si_existe(ruta):
    if os.path.exists(ruta):
        shutil.rmtree(ruta)
        print(f"📁 Carpeta eliminada: {ruta}")
