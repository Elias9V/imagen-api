# 🛰️ API CNN-LSTM para Procesamiento de Imágenes .tif

Esta API permite automatizar el flujo de trabajo para descargar imágenes satelitales `.tif` desde Google Drive, normalizarlas, dividirlas en parches, almacenarlas en PostgreSQL y gestionarlas mediante una interfaz REST construida con FastAPI.

## 📁 Estructura del Proyecto

app/
├── core/ # Configuración y utilidades generales
├── db/ # Lógica de base de datos (modelos, conexión, CRUD)
├── services/ # Servicios para limpieza, Drive, normalización, parches
├── main.py # Arranque de la API
├── routes.py # Rutas definidas de FastAPI
data/
├── raw/ # Descargas originales desde Google Drive
├── normalized/ # Imágenes normalizadas
├── patches/ # Parches generados (128x128)
.env # Variables de entorno (.env)
credentials.json # Credenciales de acceso a Google Drive
requirements.txt # Dependencias del proyecto


---

## ⚙️ Requisitos

- Python 3.10+
- PostgreSQL (Aiven o local)
- Cuenta de Google Cloud con API habilitada para Google Drive
- Archivo `credentials.json` con permisos a la carpeta compartida

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-cnn-lstm-api.git
cd proyecto-cnn-lstm-api

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API

uvicorn app.main:app --reload

# Accede a la documentación interactiva en:
📄 http://127.0.0.1:8000/docs

# Endpoints disponibles
Método	    Ruta	                Descripción
POST	    /procesar	            Descarga, normaliza, parchea y almacena imagen .tif
GET	        /listar	                Lista todas las imágenes normalizadas con parches
GET	        /buscar_por_id/{id}	    Busca imagen y sus parches por ID
DELETE	    /eliminar/{id}	        Elimina imagen y todos sus parches por ID
POST	    /generar_imagen	        Genera una nueva imagen apilada desde Earth Engine con fechas y zona dadas "exporta a Google Drive".
GET	        /descargar_normalizado/{id}	        Descarga el archivo .tif normalizado almacenado en PostgreSQL.
GET	        /descargar_parche/{id}	            Descarga un archivo de parche .tif por su ID desde la base de datos.

# Modelo CNN-LSTM
Aunque esta API no ejecuta directamente el modelo CNN-LSTM, prepara y estructura los datos como input para dicho modelo:
Normaliza valores de 10 bandas + DEM
Crea parches 128x128 con múltiples capas
Almacena metadatos estructurados
