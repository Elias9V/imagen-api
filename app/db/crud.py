# crud.py
import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from .connection import get_connection

load_dotenv(find_dotenv(), override=True)

DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'sslmode': 'require'
}

def conectar_db():
    return psycopg2.connect(**DB_CONFIG)

def insertar_imagen(nombre_archivo, ruta_local):
    with open(ruta_local, "rb") as f:
        contenido_binario = f.read()

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO imagen_normalizada (nombre_archivo, ruta_local, archivo, fecha_subida)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP) RETURNING id;
    """, (nombre_archivo, ruta_local, psycopg2.Binary(contenido_binario)))
    imagen_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return imagen_id

def obtener_archivo_binario(id):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT nombre_archivo, archivo FROM imagen_normalizada WHERE id = %s", (id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado if resultado else None

def insertar_parche(imagen_id, nombre_parche, ruta_local):
    # Leer el archivo binario
    with open(ruta_local, "rb") as f:
        archivo_binario = f.read()

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO parche (imagen_normalizada_id, nombre_parche, ruta_local, archivo)
        VALUES (%s, %s, %s, %s);
    """, (imagen_id, nombre_parche, ruta_local, psycopg2.Binary(archivo_binario)))
    conn.commit()
    cur.close()
    conn.close()

def obtener_parche_binario(parche_id):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT nombre_parche, archivo FROM parche WHERE id = %s", (parche_id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado


def guardar_en_bd(ruta_normalizada, carpeta_patches):
    nombre_archivo = os.path.basename(ruta_normalizada)
    ruta_normalizada = ruta_normalizada.replace("\\", "/")
    imagen_id = insertar_imagen(nombre_archivo, ruta_normalizada)

    for patch_name in sorted(os.listdir(carpeta_patches)):
        ruta_patch = os.path.join(carpeta_patches, patch_name).replace("\\", "/")
        insertar_parche(imagen_id, patch_name, ruta_patch)

    print(f"✅ Guardado en BD: Imagen ID {imagen_id}, {len(os.listdir(carpeta_patches))} parches")
    
def obtener_imagenes():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre_archivo, ruta_local, fecha_subida FROM imagen_normalizada ORDER BY fecha_subida DESC;
    """)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def listar_imagenes():
    conn = conectar_db()
    cur = conn.cursor()

    # 1. Obtener imágenes
    cur.execute("""
        SELECT id, nombre_archivo, fecha_subida
        FROM imagen_normalizada
        ORDER BY fecha_subida DESC;
    """)
    imagenes = cur.fetchall()

    resultado = []

    # 2. Obtener parches por cada imagen
    for imagen in imagenes:
        imagen_id, nombre_archivo, fecha_subida = imagen

        cur.execute("""
            SELECT nombre_parche FROM parche
            WHERE imagen_normalizada_id = %s
            ORDER BY nombre_parche;
        """, (imagen_id,))
        parches = [fila[0] for fila in cur.fetchall()]

        resultado.append({
            "id": imagen_id,
            "nombre_archivo": nombre_archivo,
            "fecha_subida": fecha_subida.isoformat() if fecha_subida else None,
            "parches": parches
        })

    cur.close()
    conn.close()
    return resultado



def buscar_imagen_por_id(imagen_id):
    conn = conectar_db()
    cur = conn.cursor()

    # Buscar la imagen
    cur.execute("""
        SELECT id, nombre_archivo, ruta_local, fecha_subida 
        FROM imagen_normalizada 
        WHERE id = %s;
    """, (imagen_id,))
    imagen = cur.fetchone()

    if not imagen:
        cur.close()
        conn.close()
        return None

    # Buscar los parches asociados
    cur.execute("""
        SELECT nombre_parche 
        FROM parche 
        WHERE imagen_normalizada_id = %s
        ORDER BY nombre_parche ASC;
    """, (imagen_id,))
    parches = [fila[0] for fila in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "id": imagen[0],
        "nombre_archivo": imagen[1],
        "ruta_local": imagen[2],
        "fecha_subida": str(imagen[3]),
        "parches": parches
    }



def eliminar_imagen_y_patches(imagen_id):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM parche WHERE imagen_normalizada_id = %s", (imagen_id,))
    cur.execute("DELETE FROM imagen_normalizada WHERE id = %s", (imagen_id,))
    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Imagen con ID {imagen_id} y sus parches eliminados.")

def obtener_ruta_local(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ruta_local FROM imagen_normalizada WHERE id = %s", (id,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    if resultado:
        ruta = resultado[0].replace("\\", "/")  # <- corrige las rutas si tienen backslash
        return ruta
    return None
