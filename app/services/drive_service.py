# services/drive_service.py
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from app.services.cleaner import eliminar_archivo_si_existe

FOLDER_ID = '1CfzuB1vHHfvJM9FdOCmCYYBOPdCwsYVY'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'


def obtener_servicio_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)


def obtener_ultimo_tif(service):
    resultados = service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='image/tiff'",
        orderBy='createdTime desc',
        pageSize=1,
        fields="files(id, name)"
    ).execute()
    archivos = resultados.get('files', [])
    if not archivos:
        return None
    return archivos[0]  # solo uno


def descargar_archivo_tif(service, archivo_id, nombre_destino):
    eliminar_archivo_si_existe(nombre_destino)
    request = service.files().get_media(fileId=archivo_id)
    fh = io.FileIO(nombre_destino, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    hecho = False
    while not hecho:
        status, hecho = downloader.next_chunk()
        print(f"Descargando... {int(status.progress() * 100)}%")
    fh.close()
    print(f"✅ Archivo descargado como {nombre_destino}")


def descargar_ultimo_tif_drive():
    service = obtener_servicio_drive()
    archivo = obtener_ultimo_tif(service)
    if not archivo:
        raise Exception("⚠ No se encontró ningún archivo .tif en la carpeta de Drive.")

    nombre_local = archivo['name']
    carpeta = "data/raw"
    os.makedirs(carpeta, exist_ok=True)
    ruta_local = os.path.join(carpeta, nombre_local)

    descargar_archivo_tif(service, archivo['id'], ruta_local)
    return ruta_local
