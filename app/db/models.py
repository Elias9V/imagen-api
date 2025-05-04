from app.db.connection import get_connection

def crear_tablas():
    conn = get_connection()
    cur = conn.cursor()

    # Tabla de imágenes normalizadas (con campo 'archivo')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS imagen_normalizada (
            id SERIAL PRIMARY KEY,
            nombre_archivo VARCHAR,
            ruta_local TEXT,
            archivo BYTEA,  -- Archivo .tif normalizado
            fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Tabla de parches generados (con campo 'archivo')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parche (
            id SERIAL PRIMARY KEY,
            imagen_normalizada_id INTEGER REFERENCES imagen_normalizada(id) ON DELETE CASCADE,
            nombre_parche VARCHAR,
            ruta_local TEXT,
            archivo BYTEA  -- Archivo del parche
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    crear_tablas()
