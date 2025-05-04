import ee
import uuid
from datetime import datetime

credentials = ee.ServiceAccountCredentials(
    'drive-access-bot@imagenapi-458700.iam.gserviceaccount.com',
    'credentials.json'  # El archivo que ya tienes en tu proyecto (NO lo subas a GitHub público)
)
ee.Initialize(credentials)

def generar_y_exportar_imagen(fecha_inicio: str, fecha_fin: str, coordenadas: list):
    zona = ee.Geometry.Polygon([coordenadas])

    s2 = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(zona) \
        .filterDate(fecha_inicio, fecha_fin) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

    if s2.size().getInfo() == 0:
        return {"status": "no_images", "message": "⚠ No hay imágenes en ese rango."}

    imagen = ee.Image(s2.first())
    elevacion = ee.Image('NASA/NASADEM_HGT/001').select('elevation').clip(zona).unmask(0).rename('elevacion')
    pendiente = ee.Terrain.slope(elevacion).clip(zona).unmask(0).rename('pendiente')

    imagen_apilada = imagen.select(['B2','B3','B4','B5','B6','B7','B8','B11']) \
        .addBands(elevacion).addBands(pendiente).toFloat().clip(zona)

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    unico_id = uuid.uuid4().hex[:6]
    nombre_base = f"stack_{fecha}_{unico_id}"

    exportacion = ee.batch.Export.image.toDrive(
        image=imagen_apilada,
        description=f"Export_{nombre_base}",
        folder='CNN_LSTM',
        fileNamePrefix=nombre_base,
        region=zona,
        scale=10,
        maxPixels=1e13
    )

    exportacion.start()
    return {
        "status": "started",
        "nombre_archivo": f"{nombre_base}.tif",
        "mensaje": "🚀 Exportación iniciada. Verifica en https://code.earthengine.google.com/tasks"
    }
